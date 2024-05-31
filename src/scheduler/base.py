import abc


class BaseShopJobScheduler(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_order(self):
        raise NotImplementedError

    def schedule(self):
        pass
