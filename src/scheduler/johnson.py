import random

from src.job import Job
from src.machine import Machine
from src.scheduler.base import BaseShopJobScheduler


class JohnsonShopJobScheduler(BaseShopJobScheduler):

    def get_job_order(self) -> list[Job]:
        k = len(self.machines) // 2
        fictitious_times = []
        for job in self.jobs:
            t1 = sum([job.process_times[m] for m in self.machines[:k]])
            t2 = sum([job.process_times[m] for m in self.machines[k:]])
            fictitious_times.append([t1, t2])
        print("Fictitious Machines:")
        for m1, m2 in fictitious_times:
            print(f"M1 = {m1:<6} M2 = {m2}")
        print(15 * "-")
        return self._johnson_algorithm(fictitious_times)

    def _johnson_algorithm(self, processing_times):
        num_jobs = len(processing_times)
        job_indices = list(range(num_jobs))

        left = []
        right = []

        while job_indices:
            # Find the job with the smallest time
            job_index = min(job_indices, key=lambda x: min(processing_times[x]))
            job_indices.remove(job_index)

            if processing_times[job_index][0] < processing_times[job_index][1]:
                left.append(job_index)
            else:
                right.append(job_index)

        # Left list goes in the front, right list goes in the back
        job_order = left + right[::-1]
        return [self.jobs[i] for i in job_order]

    def get_machine_order(self) -> list[Machine]:
        k = len(self.machines) // 2
        length = len(self.machines)
        machine_order: list[Machine] = random.sample(
            self.machines[:k], k
        ) + random.sample(self.machines[k:], length - k)
        return machine_order
