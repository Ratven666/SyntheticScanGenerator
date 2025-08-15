from abc import ABC, abstractmethod

import numpy as np

from CONFIG import RANDOM_SEED


class PointsFilterABC(ABC):

    def __init__(self, random_seed=RANDOM_SEED):
        self.scan_generator_obj = None
        self.base_direction = None
        self.ray_origins = None
        self.base_directions_vectors = None
        self.mse_directions_vectors = None
        self.locations = None
        self.index_ray = None
        self.index_tri = None
        self.random_seed = random_seed

    @abstractmethod
    def _filter_logic(self, point_index):
        pass

    def get_points_mask(self,
                        scan_generator_obj,
                        base_direction,
                        ray_origins,
                        base_directions_vectors,
                        mse_directions_vectors,
                        locations,
                        index_ray,
                        index_tri):
        self.scan_generator_obj = scan_generator_obj
        self.base_direction = base_direction
        self.ray_origins = ray_origins
        self.base_directions_vectors = base_directions_vectors
        self.mse_directions_vectors = mse_directions_vectors
        self.locations = locations
        self.index_ray = index_ray
        self.index_tri = index_tri

        if self.random_seed is not None:
            np.random.seed(self.random_seed)

        vectorized_filter = np.vectorize(self._filter_logic)
        mask = vectorized_filter(point_index=range(len(self.locations)))
        print(mask)
        print(len(mask))
        return mask
