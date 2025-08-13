from abc import ABC, abstractmethod

import numpy as np

from CONFIG import RANDOM_SEED


class ScannerABC(ABC):

    def __init__(self, random_seed=RANDOM_SEED):
        self.random_seed = random_seed
        self.max_range = None

    @abstractmethod
    def get_scanner_directions(self, *scan_parameters, **kw_scan_parameters):
        if self.random_seed is not None:
            np.random.seed(self.random_seed)
