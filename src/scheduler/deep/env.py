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
        self.action_space = spaces.Discrete(len(machines) * len(jobs))
        self.observation_space = spaces.Box(low=0, high=1, shape=(len(jobs), len(machines)), dtype=np.float32)
        self.state = self._get_initial_state()
        self.machine_queues = {machine: MachineQueue(machine) for machine in machines}
        self.machines_last_due_times = defaultdict(float)

    def _get_initial_state(self):
        # Example initial state: matrix of zeros
        return np.zeros((len(self.jobs), len(self.machines)))

    def step(self, action):
        job_id = action // len(self.machines)
        machine_id = action % len(self.machines)

        job = self.jobs[job_id]
        machine = self.machines[machine_id]

        # Create a task and assign it to the machine's queue
        exec_time = job.get_machine_process_time(machine)
        task = Task(job, exec_time)
        task.arrival = max(self.machines_last_due_times[machine], self.state[job_id, machine_id])
        self.machines_last_due_times[machine] = task.due
        self.machine_queues[machine].push(task)

        # Update the state to reflect the scheduling
        self.state[job_id, machine_id] = task.due

        # Calculate reward
        reward = -self._calculate_make_span()

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
        self.machines_last_due_times = defaultdict(float)
        return self.state

    def _calculate_make_span(self):
        # The make-span is the maximum time any machine finishes its tasks
        make_span = max(queue.last_task_due() for queue in self.machine_queues.values())
        return make_span

    def _is_done(self):
        # Check if all jobs are scheduled
        scheduled_tasks = [task for queue in self.machine_queues.values() for task in queue.tasks]
        return len(scheduled_tasks) == len(self.jobs) * len(self.machines)
