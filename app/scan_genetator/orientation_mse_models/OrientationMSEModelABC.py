from abc import ABC, abstractmethod

import numpy as np

from CONFIG import RANDOM_SEED
from app.scanners.ScannerABC import ScannerABC


class OrientationMSEModelABC(ABC):

    def __init__(self, scanner: ScannerABC, orientation_mse_parameters_dict: (dict, None), random_seed=RANDOM_SEED):
        self.scanner = scanner
        self.orientation_mse_parameters_dict = orientation_mse_parameters_dict
        self.random_seed = random_seed
        if self.random_seed is not None:
            np.random.seed(self.random_seed)

    @abstractmethod
    def calculate_orientation_mse_location(self, ray_origins, locations, index_rays):
        pass
