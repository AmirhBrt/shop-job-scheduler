from src.scheduler.base import BaseShopJobScheduler
from src.job import Job
from src.machine import Machine


class DeepRLScheduler(BaseShopJobScheduler):
    def __init__(self, machines: list[Machine], jobs: list[Job]):
        super().__init__(machines, jobs)

    def get_job_order(self) -> list[Job]:
        pass

    def get_machine_order(self) -> list[Machine]:
        pass
