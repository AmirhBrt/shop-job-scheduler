import abc

from src.job import Job
from src.machine import Machine


class BaseShopJobScheduler(abc.ABC):
    def __init__(self, machines: list[Machine], jobs: list[Job]):
        pass

    @abc.abstractmethod
    def get_order(self):
        raise NotImplementedError

    def schedule(self):
        pass
