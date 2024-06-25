import random

from src.job import Job
from src.machine import Machine
from src.scheduler.base import BaseShopJobScheduler


class RandomShopJobScheduler(BaseShopJobScheduler):
    def get_job_order(self) -> list[Job]:
        jobs = [job for job in self.jobs]
        random.shuffle(jobs)
        return jobs

    def get_machine_order(self) -> list[Machine]:
        machines = [machine for machine in self.machines]
        random.shuffle(machines)
        return machines
