import json

from src.machine import Machine
from src.scheduler import RandomShopJobScheduler, JohnsonShopJobScheduler
from src.job import Job


class Runner:
    def __init__(self, file_path: str):
        self.__file_path = file_path
        with open(file_path) as f:
            self.__config = json.load(f)

    def __create_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        for data in self.__config.get("jobs"):
            process_times = {}
            for process_time in data["process times"]:
                process_times[process_time["machine pk"]] = process_time["amount"]
            job = Job(
                pk=data["pk"],
                process_times=process_times
            )
            jobs.append(job)
        return jobs

    def __create_machines(self) -> list[Machine]:
        machines: list[Machine] = []
        for data in self.__config.get("machines"):
            m = Machine(
                pk=data["pk"],
            )
            machines.append(m)
        return machines

    @staticmethod
    def __get_algorithms():
        return ["random", "johnson", ]

    def run(self):
        jobs: list[Job] = self.__create_jobs()
        machines: list[Machine] = self.__create_machines()
        if self.__config["algorithm"] == "random":
            RandomShopJobScheduler(
                machines=machines,
                jobs=jobs,
            )
        elif self.__config["algorithm"] == "johnson":
            JohnsonShopJobScheduler(
                machines=machines,
                jobs=jobs,
            )
        raise ValueError(f"Invalid algorithm chosen! Must be from one of {self.__get_algorithms()}")
