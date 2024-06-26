import json

from src.job import Job
from src.machine import Machine
from src.scheduler import JohnsonShopJobScheduler, RandomShopJobScheduler, GeneticShopJobScheduler, DQNScheduler
from src.scheduler.deep.agent import DQNAgent


class Runner:
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__machines: dict[int: Machine] = dict()
        with open(file_path) as f:
            self.__config = json.load(f)

    def create_jobs(self) -> list[Job]:
        jobs = list()
        for data in self.__config.get("jobs"):
            process_times = {}
            for process_time in data["process times"]:
                machine_pk = process_time["machine pk"]
                process_times[self.__machines[machine_pk]] = process_time["amount"]
            job = Job(
                pk=data["pk"],
                process_times=process_times
            )
            jobs.append(job)
        return jobs

    def create_machines(self) -> list[Machine]:
        machines = list()
        for data in self.__config.get("machines"):
            m = Machine(
                pk=data["pk"],
            )
            machines.append(m)
            self.__machines[data["pk"]] = m
        return machines

    @staticmethod
    def __get_algorithms():
        return ["random", "johnson", "genetic", "deep", ]

    def run(self):
        machines = self.create_machines()
        jobs = self.create_jobs()
        if self.__config["algorithm"] == "random":
            RandomShopJobScheduler(
                machines=machines,
                jobs=jobs,
            ).schedule()
        elif self.__config["algorithm"] == "johnson":
            JohnsonShopJobScheduler(
                machines=machines,
                jobs=jobs,
            ).schedule()
        elif self.__config["algorithm"] == "genetic":
            GeneticShopJobScheduler(
                machines=machines,
                jobs=jobs,
            ).schedule()
        elif self.__config["algorithm"] == "deep":
            agent = DQNAgent(jobs)
            # TODO: You must train agent before running it
            DQNScheduler(
                machines=machines,
                jobs=jobs,
                agent=agent
            ).schedule()
        else:
            raise ValueError(f"Invalid algorithm chosen! Must be from one of {self.__get_algorithms()}")
