from src.machine import Machine


class Job:
    def __init__(self, pk, process_times: dict[Machine: float]):
        self.pk = pk
        self.process_times = process_times

    def get_machine_process_time(self, machine: Machine):
        return self.process_times.get(machine, 0)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.pk == other.pk:
                return True
        return False

    def __hash__(self):
        return hash(self.pk)

    def __str__(self):
        return f"J{self.pk}"
