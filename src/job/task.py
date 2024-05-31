from .job import Job


class Task:
    def __init__(self, job: Job, exec_time: float):
        self.job = job
        self.exec_time: float = exec_time
        self.__arrival: float = 0

    @property
    def arrival(self) -> float:
        return self.__arrival

    @arrival.setter
    def arrival(self, value: float):
        self.__arrival = value

    @property
    def due(self) -> float:
        return self.__arrival + self.exec_time
