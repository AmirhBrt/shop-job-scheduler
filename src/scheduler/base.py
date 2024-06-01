import abc

from src.job import Job
from src.machine import Machine
from src.queue import MachineQueue


class BaseShopJobScheduler(abc.ABC):
    def __init__(self, machines: list[Machine], jobs: list[Job]):
        self.machines = machines
        self.jobs = jobs
        self.queues: dict[Machine: MachineQueue] = {m: MachineQueue(m) for m in self.machines}

    @abc.abstractmethod
    def get_job_order(self) -> list[Job]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_machine_order_for_job(self, job: Job, machines_last_due_times: dict[Machine: float]) -> list[Machine]:
        raise NotImplementedError

    @abc.abstractmethod
    def schedule(self):
        raise NotImplementedError
