import numpy as np

from CONFIG import RANDOM_SEED
from app.scan_genetator.real_location_calculator.distance_mse_models.BaseDistanceMSEModel import BaseDistanceMSEModel
from app.scan_genetator.real_location_calculator.points_filters_models.FalsePointsFilters import FalsePointsFilters


class RealLocationCalculator:

    def __init__(self,
                 distance_mse_model=BaseDistanceMSEModel(random_seed=RANDOM_SEED),
                 point_filter_model=FalsePointsFilters(random_seed=RANDOM_SEED),
                 ):
        self._distance_mse_model = distance_mse_model
        self._point_filter_model = point_filter_model

        self.scan_generator_obj = None
        self.base_direction = None
        self.ray_origins = None
        self.base_directions_vectors = None
        self.mse_directions_vectors = None
        self.locations = None
        self.index_ray = None
        self.index_tri = None

    def _get_filtered_points(self):
        mask = self._point_filter_model.get_points_mask(real_distance_calculator_obj=self)
        self.locations, self.index_ray, self.index_tri = (self.locations[mask],
                                                          self.index_ray[mask],
                                                          self.index_tri[mask])
        self.ray_origins, self.base_direction = self.ray_origins[mask], self.base_direction[mask]
        self.base_directions_vectors = self.base_directions_vectors[mask]
        self.mse_directions_vectors = self.mse_directions_vectors[mask]
        return mask

    def _calk_mse_locations(self, mse_distances):
        azimuth_rad = np.deg2rad(self.base_direction[:, 0])
        zenith_rad = np.deg2rad(self.base_direction[:, 1])
        sin_zenith = np.sin(zenith_rad)
        x = mse_distances * sin_zenith * np.cos(azimuth_rad)
        y = mse_distances * sin_zenith * np.sin(azimuth_rad)
        z = mse_distances * np.cos(zenith_rad)
        mse_locations = self.ray_origins + np.column_stack((x, y, z))
        return mse_locations

    def calculate_real_point_location(self,
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

        mask = self._get_filtered_points()

        mse_distances = self._distance_mse_model.calculate_mse_distances(real_distance_calculator_obj=self)
        mse_locations = self._calk_mse_locations(mse_distances)
        return mse_locations, self.index_ray, self.index_tri
