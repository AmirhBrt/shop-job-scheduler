import gym
import numpy as np
from gym import spaces

from src.job import Job, Task
from src.machine import Machine
from src.queue import MachineQueue
from src.scheduler.base import BaseShopJobScheduler


class SchedulingEnv(gym.Env):
    def __init__(self, machines: list[Machine], jobs: list[Job]):
        super(SchedulingEnv, self).__init__()
        self.machines = machines
        self.jobs = jobs
        self.queues = {machine: MachineQueue(machine) for machine in machines}
        self.state = self._get_initial_state()
        self.action_space = spaces.Discrete(len(machines) * len(jobs))
        self.observation_space = spaces.Box(low=0, high=1, shape=(len(machines), len(jobs)), dtype=np.float32)

    def _get_initial_state(self) -> np.ndarray:
        # Initialize the state representation
        return np.zeros((len(self.machines), len(self.jobs)))

    def step(self, action):
        # Apply the action and compute the new state, reward, and done flag
        job_index = action // len(self.machines)
        machine_index = action % len(self.machines)
        job = self.jobs[job_index]
        machine = self.machines[machine_index]

        task = Task(job, job.get_machine_process_time(machine))
        self.queues[machine].push(task)

        self.state = self._get_state_representation()
        reward = self._compute_reward()
        done = self._check_done()

        return self.state, reward, done, {}

    def reset(self):
        self.queues = {machine: MachineQueue(machine) for machine in self.machines}
        self.state = self._get_initial_state()
        return self.state

    def _get_state_representation(self):
        # Update the state representation based on the current state of the queues
        state = np.zeros((len(self.machines), len(self.jobs)))
        for m_index, (machine, queue) in enumerate(self.queues.items()):
            for j_index, job in enumerate(self.jobs):
                if job in [task.job for task in queue.tasks]:
                    state[m_index][j_index] = 1
        return state

    def _compute_reward(self):
        # Calculate the reward based on the makespan (total completion time)
        total_completion_time = max(queue.last_task_due() for queue in self.queues.values())
        reward = -total_completion_time  # Negative reward because we want to minimize it
        return reward

    def _check_done(self):
        # Check if all jobs have been scheduled
        all_jobs_scheduled = all(len(queue.tasks) == len(self.jobs) for queue in self.queues.values())
        return all_jobs_scheduled


class DeepRLScheduler(BaseShopJobScheduler):
    def __init__(self, machines: list[Machine], jobs: list[Job]):
        super().__init__(machines, jobs)

    def get_job_order(self) -> list[Job]:
        pass

    def get_machine_order(self) -> list[Machine]:
        pass
