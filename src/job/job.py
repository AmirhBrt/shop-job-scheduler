

class Job:
    def __init__(self, pk):
        self.pk = pk

    def __str__(self):
        return f"J{self.pk}"
