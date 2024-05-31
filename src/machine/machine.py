

class Machine:
    def __init__(self, pk):
        self.pk = pk

    def __str__(self):
        return f"M{self.pk}"
