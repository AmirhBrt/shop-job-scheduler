from .base import BaseShopJobScheduler


class JohnsonShopJobScheduler(BaseShopJobScheduler):
    def schedule(self):
        order = self.get_job_order()
        machines_last_due_times: dict[Machine: float] = {}
        for machine in self.machines:
            machines_last_due_times[machine] = 0
        for job in order:
            machines_last_due_list = []
            for key, value in machines_last_due_times.items():
                machines_last_due_list.append((key, value))
            machines_last_due_list.sort(key=lambda item: item[1])

    def get_job_order(self):
        pass
