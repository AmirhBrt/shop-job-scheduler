import random

from src.job import Job
from src.machine import Machine
from .base import BaseShopJobScheduler


class RandomShopJobScheduler(BaseShopJobScheduler):
    def get_machine_order(self) -> list[Machine]:
        machines = [machine for machine in self.machines]
        order = []
        while machines:
            item = random.choice(machines)
            order.append(item)
            machines.remove(item)
        return order

    def get_job_order(self) -> list[Job]:
        jobs = [job for job in self.jobs]
        order = []
        while jobs:
            item = random.choice(jobs)
            order.append(item)
            jobs.remove(item)
        return order
