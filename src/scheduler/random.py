import random

from src.job import Job
from src.machine import Machine
from src.scheduler.base import BaseShopJobScheduler


class RandomShopJobScheduler(BaseShopJobScheduler):
    def get_job_order(self) -> list[Job]:
        jobs = self.jobs[:]
        random.shuffle(jobs)
        return jobs

    def get_machine_order(self) -> list[Machine]:
        machines = self.machines[:]
        random.shuffle(machines)
        return machines
