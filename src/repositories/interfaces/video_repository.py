import abc

class VideoRepositoryInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_url(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def add(self):
        raise NotImplementedError()
