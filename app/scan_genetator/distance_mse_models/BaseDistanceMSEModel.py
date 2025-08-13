import numpy as np

from app.scan_genetator.distance_mse_models.DistanceMSEModelABC import DistanceMSEModelABC


class BaseDistanceMSEModel(DistanceMSEModelABC):

    def calculate_distance_errors(self,
                                  scan_generator_obj,
                                  base_direction,
                                  ray_origins,
                                  base_directions_vectors,
                                  mse_directions_vectors,
                                  locations,
                                  index_ray,
                                  index_tri):
        distance_accuracy = scan_generator_obj.scanner.distance_accuracy
        distances_errors = np.random.normal(0, distance_accuracy, size=len(index_ray))
        return distances_errors
