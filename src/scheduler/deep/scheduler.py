import numpy as np

from src.scheduler.base import BaseShopJobScheduler
from src.scheduler.deep.env import JobSchedulingEnv


class DQNScheduler(BaseShopJobScheduler):
    def __init__(self, machines, jobs, agent):
        super().__init__(machines, jobs)
        self.agent = agent
        self.env = JobSchedulingEnv(machines, jobs)

    def get_job_order(self):
        state = self._get_initial_state()
        job_order = []
        actions = set()
        for _ in range(len(self.jobs)):
            q_values = self.agent.model.predict(state)[0]
            q_values = filter(lambda x: x[0] not in actions, enumerate(q_values))
            action = max(q_values, key=lambda x: x[1])[0]
            actions.add(action)
            print(f"Action = {action}")
            job_order.append(self.jobs[action])
            next_state, _, _, _ = self.env.step(action)

            state = np.reshape(next_state, [1, len(self.jobs)])
        return job_order

    def get_machine_order(self):
        return self.machines

    def _get_initial_state(self):
        return np.zeros((1, len(self.jobs)))
