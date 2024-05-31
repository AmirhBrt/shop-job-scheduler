from src.job import Task
from src.machine import Machine


class MachineQueue:
    def __init__(self, machine: Machine):
        self.machine: Machine = machine
        self.tasks: list[Task] = []

    def push(self, task: Task):
        self.tasks.append(task)

    def pop(self):
        self.tasks.pop(0)

    def idle_time(self):
        sum_idle_time = 0
        last_arrival = 0
        for task in self.tasks:
            sum_idle_time += last_arrival - task.arrival
            last_arrival = task.arrival
        return sum_idle_time
