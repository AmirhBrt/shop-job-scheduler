from .base import BaseShopJobScheduler
from src.machine import Machine
from src.job import Job, Task
import random


class JohnsonShopJobScheduler(BaseShopJobScheduler):

    def get_job_order(self):
        k = len(self.machines) // 2
        fictitious_times = []
        for job in self.jobs:
            T1 = sum([job.process_times[m] for m in self.machines[:k]])
            T2 = sum([job.process_times[m] for m in self.machines[k:]])
            fictitious_times.append([T1, T2])
        return self._johnsons_algorithm(fictitious_times)

    def _johnsons_algorithm(self, processing_times):
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

    def get_machine_order_for_job(
        self, job: Job, machines_last_due_times: dict[Machine:float]
    ) -> list[Machine]: ...

    def schedule(self):
        k = len(self.machines) // 2
        length = len(self.machines)
        job_orders: list[Job] = self.get_job_order()
        print(f"Order = {list(map(lambda x: x.pk, job_orders))}")
        machines_last_due_times: dict[Machine:float] = {}
        for machine in self.machines:
            machines_last_due_times[machine] = 0
        machine_orders: list[Machine] = random.sample(
            self.machines[:k], k
        ) + random.sample(self.machines[k:], length - k)
        for job in job_orders:
            last = 0
            for _, m in enumerate(machine_orders):
                t = Task(job, job.process_times[m])
                t.arrival = max(machines_last_due_times[m], last)
                machines_last_due_times[m] = t.arrival + job.process_times[m]
                self.queues[m].push(t)
                last = machines_last_due_times[m]
        print(15 * "-")
        for machine, q in self.queues.items():
            print(f"Machine {machine.pk}")
            for t in q.tasks:
                print(
                    f"job = {t.job.pk} -- arrival {t.arrival} -- exec = {t.exec_time}"
                )
            print(15 * "-")
