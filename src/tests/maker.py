import json
import random


class TestMaker:
    def __init__(self, algorithm: str, machines_count: int = 2, jobs_count: int = 10):
        self.algorithm = algorithm
        self.machine_config = '{\"pk\"={}}'
        self.job_config = '{\"pk\"={}, \"process times\"=[{}]'
        self.machines_count = machines_count
        self.jobs_count = jobs_count

    def __create_machines(self):
        machines = []
        for i in range(1, self.machines_count + 1):
            data = {
                "pk": i,
            }
            machines.append(data)
        return machines

    def __create_jobs(self):
        jobs = []
        for i in range(1, self.jobs_count + 1):
            process_times = []
            for j in range(1, self.machines_count + 1):
                data = {
                    "machine pk": j,
                    "amount": random.randint(1, 10),
                }
                process_times.append(data)
            data = {
                "pk": i,
                "process times": process_times
            }
            jobs.append(data)
        return jobs

    def create_test(self, file_path: str):
        with open(file_path, 'w') as f:
            data = {
                "algorithm": self.algorithm,
                "machines": self.__create_machines(),
                "jobs": self.__create_jobs(),
            }
            json.dump(data, f, indent=2)
