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

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if (self.arrival, self.exec_time, self.job) == (other.arrival, other.exec_time, other.job):
                return True
        return False

    def __hash__(self):
        return hash((self.arrival, self.exec_time, self.job))
