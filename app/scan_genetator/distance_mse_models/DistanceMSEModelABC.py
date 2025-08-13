from abc import ABC, abstractmethod

import numpy as np

from CONFIG import RANDOM_SEED


class DistanceMSEModelABC(ABC):

    def __init__(self, random_seed=RANDOM_SEED):
        self.random_seed = random_seed
        if self.random_seed is not None:
            np.random.seed(self.random_seed)

    @abstractmethod
    def calculate_distance_errors(self,
                                  scan_generator_obj,
                                  base_direction,
                                  ray_origins,
                                  base_directions_vectors,
                                  mse_directions_vectors,
                                  locations,
                                  index_ray,
                                  index_tri):
        pass
