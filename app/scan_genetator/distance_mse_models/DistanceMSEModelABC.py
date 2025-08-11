from abc import ABC, abstractmethod


class DistanceMSEModelABC(ABC):

    @abstractmethod
    def f(self):
        pass