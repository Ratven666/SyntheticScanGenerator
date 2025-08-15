from abc import ABC, abstractmethod

import numpy as np

from app.scan_genetator.real_location_calculator.RLCUtilModelsClass import RLCUtilModelsClass


class DistanceMSEModelABC(ABC, RLCUtilModelsClass):

    @abstractmethod
    def _calculate_distance_errors(self):
        pass

    def calculate_mse_distances(self, real_distance_calculator_obj):
        self._init_model_data(real_distance_calculator_obj=real_distance_calculator_obj)

        distances = np.linalg.norm(self.locations - self.ray_origins, axis=1)
        distances_errors = self._calculate_distance_errors()
        return distances + distances_errors
