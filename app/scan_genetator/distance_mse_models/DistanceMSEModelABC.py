from abc import ABC, abstractmethod

import numpy as np

from CONFIG import RANDOM_SEED
from app.scan_genetator.points_filters.FalsePointsFilters import FalsePointsFilters


class DistanceMSEModelABC(ABC):

    def __init__(self,
                 point_filter_obj=FalsePointsFilters(random_seed=RANDOM_SEED),
                 random_seed=RANDOM_SEED):
        self.point_filter_obj = point_filter_obj
        self.scan_generator_obj = None
        self.base_direction = None
        self.ray_origins = None
        self.base_directions_vectors = None
        self.mse_directions_vectors = None
        self.locations = None
        self.index_ray = None
        self.index_tri = None
        self.random_seed = random_seed
        if self.random_seed is not None:
            np.random.seed(self.random_seed)

    @abstractmethod
    def _calculate_distance_errors(self):
        pass

    def _get_points_mask(self):
        mask = self.point_filter_obj.get_points_mask(scan_generator_obj=self.scan_generator_obj,
                                                     base_direction=self.base_direction,
                                                     ray_origins=self.ray_origins,
                                                     base_directions_vectors=self.base_directions_vectors,
                                                     mse_directions_vectors=self.mse_directions_vectors,
                                                     locations=self.locations,
                                                     index_ray=self.index_ray,
                                                     index_tri=self.index_tri,
                                                     )
        return mask

    def calculate_by_distance_mse_model(self,
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

        mask = self._get_points_mask()
        self.locations, self.index_ray, self.index_tri = locations[mask], index_ray[mask], index_tri[mask]
        self.ray_origins, self.base_direction = self.ray_origins[mask], self.base_direction[mask]

        distances_errors = self._calculate_distance_errors()
        mse_locations = self._calk_mse_locations(distances_errors)
        return mse_locations, self.index_ray, self.index_tri

    def _calk_mse_locations(self, distances_errors):
        distances = np.linalg.norm(self.locations - self.ray_origins, axis=1)
        distances += distances_errors
        azimuth_rad = np.deg2rad(self.base_direction[:, 0])
        zenith_rad = np.deg2rad(self.base_direction[:, 1])
        sin_zenith = np.sin(zenith_rad)
        x = distances * sin_zenith * np.cos(azimuth_rad)
        y = distances * sin_zenith * np.sin(azimuth_rad)
        z = distances * np.cos(zenith_rad)
        mse_locations = self.ray_origins + np.column_stack((x, y, z))
        return mse_locations
