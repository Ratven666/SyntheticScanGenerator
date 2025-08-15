import numpy as np

from app.scan_genetator.distance_mse_models.DistanceMSEModelABC import DistanceMSEModelABC


class BaseDistanceMSEModel(DistanceMSEModelABC):

    def _calculate_distance_errors(self):
        if self.random_seed is not None:
            np.random.seed(self.random_seed)
        distance_accuracy = self.scan_generator_obj.scanner.distance_accuracy
        distances_errors = np.random.normal(0, distance_accuracy, size=len(self.index_ray))
        return distances_errors
