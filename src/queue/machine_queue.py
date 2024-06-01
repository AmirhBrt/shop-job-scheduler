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

    def last_task_due(self):
        if len(self.tasks) == 0:
            return 0
        last_task = self.tasks[-1]
        return last_task.due

    def idle_time(self):
        sum_idle_time = 0
        last_arrival = 0
        for task in self.tasks:
            sum_idle_time += task.arrival - last_arrival
            last_arrival = task.due
        return sum_idle_time

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if (self.machine, self.tasks) == (other.machine, other.tasks):
                return True
        return False

    def __hash__(self):
        return hash((self.machine, self.tasks))
