import abc

from src.job import Job, Task
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
    def get_machine_order(self) -> list[Machine]:
        raise NotImplementedError

    def _schedule(self, job_orders: list[Job]) -> int:
        machines_last_due_times: dict[Machine:float] = {}
        for machine in self.machines:
            machines_last_due_times[machine] = 0
        machine_orders: list[Machine] = self.get_machine_order()
        for job in job_orders:
            last = 0
            for m in machine_orders:
                t = Task(job, job.process_times[m])
                t.arrival = max(machines_last_due_times[m], last)
                machines_last_due_times[m] = t.arrival + job.process_times[m]
                self.queues[m].push(t)
                last = machines_last_due_times[m]
    
    def schedule(self):        
        job_orders = self.get_job_order()
        self._schedule(job_orders)
        print(f"Order = {list(map(lambda j: str(j), job_orders))}")
        print(15 * "-")
        for machine, q in self.queues.items():
            print(f"Machine {machine.pk}")
            for t in q.tasks:
                print(
                    f"{str(t.job):<6} arrival = {t.arrival:<6} exec = {t.exec_time}"
                )
            print(15 * "-")
        makespan = max(self.queues.values(), key=lambda q: q.last_task_due()).last_task_due()
        print(f"Make Span = {makespan}")