from abc import ABC, abstractmethod


class ScannerABC(ABC):

    def __init__(self):
        self.name = None
        self.max_range = None
        self.angular_accuracy = None
        self.distance_accuracy = None

    @abstractmethod
    def get_scanner_directions(self, *scan_parameters, **kw_scan_parameters):
        pass
