import random

from src.job import Job, Task
from src.machine import Machine
from src.queue import MachineQueue
from .base import BaseShopJobScheduler


class RandomShopJobScheduler(BaseShopJobScheduler):
    def get_machine_order_for_job(self, job: Job, machines_last_due_times: dict[Machine: float]) -> list[Machine]:
        machines = [machine for machine in self.machines]
        order = []
        while machines:
            item = random.choice(machines)
            order.append(item)
            machines.remove(item)
        return order

    def get_job_order(self) -> list[Job]:
        jobs = [job for job in self.jobs]
        order = []
        while jobs:
            item = random.choice(jobs)
            order.append(item)
            jobs.remove(item)
        return order

    def schedule(self):
        jobs_order = self.get_job_order()
        machines_last_due_times: dict[Machine: float] = {}
        for machine in self.machines:
            machines_last_due_times[machine] = 0
        for job in jobs_order:
            machines_order = self.get_machine_order_for_job(job, machines_last_due_times)
            max_prev_due_time = machines_last_due_times[machines_order[0]]
            for machine in machines_order:
                queue = self.get_machine_queue(machine)
                task = Task(job, job.get_machine_process_time(machine))
                # todo: complete scheduling tasks

    def get_machine_queue(self, machine: Machine) -> MachineQueue:
        queue = self.queues.get(machine)
        if queue is None:
            self.queues[machine] = MachineQueue(machine)
            queue = self.queues.get(machine)
        return queue
