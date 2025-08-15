import numpy as np

from CONFIG import RANDOM_SEED


class RLCUtilModelsClass:

    def __init__(self, random_seed=RANDOM_SEED):
        self.random_seed = random_seed
        self.real_distance_calculator_obj = None

    @property
    def scan_generator_obj(self):
        return self.real_distance_calculator_obj.scan_generator_obj

    @property
    def base_direction(self):
        return self.real_distance_calculator_obj.base_direction

    @property
    def ray_origins(self):
        return self.real_distance_calculator_obj.ray_origins

    @property
    def base_directions_vectors(self):
        return self.real_distance_calculator_obj.base_directions_vectors

    @property
    def mse_directions_vectors(self):
        return self.real_distance_calculator_obj.mse_directions_vectors

    @property
    def locations(self):
        return self.real_distance_calculator_obj.locations

    @property
    def index_ray(self):
        return self.real_distance_calculator_obj.index_ray

    @property
    def index_tri(self):
        return self.real_distance_calculator_obj.index_tri

    def _init_model_data(self, real_distance_calculator_obj):
        self.real_distance_calculator_obj = real_distance_calculator_obj
        if self.random_seed is not None:
            np.random.seed(self.random_seed)
