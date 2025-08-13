from abc import ABC, abstractmethod

from app.scanners.ScannerABC import ScannerABC


class OrientationMSEModelABC(ABC):

    def __init__(self, scanner: ScannerABC, orientation_mse_parameters_dist: (dict, None)):
        self.scanner = scanner
        self.orientation_mse_parameters_diсt = orientation_mse_parameters_dist

    @abstractmethod
    def calculate_orientation_mse_location(self, ray_origins, locations, index_rays):
        pass
