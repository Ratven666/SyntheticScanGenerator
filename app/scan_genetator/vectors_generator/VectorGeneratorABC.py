from abc import ABC, abstractmethod


class VectorGeneratorABC(ABC):

    @abstractmethod
    def __init__(self, *position_data, **kw_position_data):
        pass

    @abstractmethod
    def get_vectors(self, scanner, *scan_parameters, **kw_scan_parameters):
        pass
