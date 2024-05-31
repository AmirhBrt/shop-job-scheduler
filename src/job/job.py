

class Job:
    def __init__(self, pk):
        self.pk = pk

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.pk == other.pk:
                return True
        return False

    def __hash__(self):
        return hash(self.pk)

    def __str__(self):
        return f"J{self.pk}"
