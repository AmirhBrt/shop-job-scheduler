from collections import defaultdict

import gym
import numpy as np
from gym import spaces

from src.job import Job, Task
from src.machine import Machine
from src.queue import MachineQueue


class JobSchedulingEnv(gym.Env):
    def __init__(self, machines: list[Machine], jobs: list[Job]):
        super(JobSchedulingEnv, self).__init__()
        self.machines = machines
        self.jobs = jobs
        self.action_space = spaces.Discrete(len(jobs))
        self.observation_space = spaces.Discrete(len(jobs))
        self.state = self._get_initial_state()
        self.machine_queues = {machine: MachineQueue(machine) for machine in machines}
        self.machines_last_due_times = defaultdict(float)

    def _get_initial_state(self):
        # Example initial state: matrix of zeros
        return np.zeros(len(self.jobs))

    def step(self, action):
        job_id = action

        if self.state[job_id] > 0:
            return self.state, float("-inf"), False, {}

        job = self.jobs[job_id]

        # Create a task and assign it to the machine's queue
        last = 0
        for machine in self.machines:
            exec_time = job.get_machine_process_time(machine)
            task = Task(job, exec_time)
            task.arrival = max(self.machines_last_due_times[machine], last)
            self.machines_last_due_times[machine] = task.due
            last = task.due

            self.machine_queues[machine].push(task)

            self.state[job_id] = task.due

        # Calculate reward
        reward = -last

        done = self._is_done()

        return self.state, reward, done, {}

    def render(self, mode='human'):
        for machine, queue in self.machine_queues.items():
            print(f"Machine {machine.pk}:")
            for task in queue.tasks:
                print(f"   Task {task.job.pk} arrival={task.arrival} due={task.due}")

    def reset(self, **kwargs):
        self.state = self._get_initial_state()
        self.machine_queues = {machine: MachineQueue(machine) for machine in self.machines}
        return self.state

    def _is_done(self):
        # Check if all jobs are scheduled
        scheduled_tasks = []
        for queue in self.machine_queues.values():
            scheduled_tasks.extend(queue.tasks)

        return len(scheduled_tasks) == len(self.jobs) * len(self.machines)
