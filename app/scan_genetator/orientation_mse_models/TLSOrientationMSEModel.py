import numpy as np
from typing import Tuple

from app.scan_genetator.orientation_mse_models.OrientationMSEModelABC import OrientationMSEModelABC
from app.scanners.ScannerABC import ScannerABC


class TLSOrientationMSEModel(OrientationMSEModelABC):

    def __init__(self, scanner: ScannerABC, orientation_mse_parameters_dict: (dict, None), random_seed=None):
        super().__init__(scanner, orientation_mse_parameters_dict, random_seed)
        self.base_translation = None
        self.base_rotation_angles = None
        self.mse_translation = None
        self.mse_rotation_angles = None
        self._init_params()

    def _init_params(self):
        try:
            self.base_translation = np.asarray(self.orientation_mse_parameters_dict["base_translation"],
                                               dtype=np.float64)
            self.base_rotation_angles = np.asarray(self.orientation_mse_parameters_dict["base_rotation_angles"],
                                                   dtype=np.float64)
            self.mse_translation = np.asarray(self.orientation_mse_parameters_dict["mse_translation"],
                                              dtype=np.float64)
            self.mse_rotation_angles = np.asarray(self.orientation_mse_parameters_dict["mse_rotation_angles"],
                                                  dtype=np.float64)
        except KeyError as e:
            raise ValueError(f"Отсутствует обязательный параметр: {e}") from None
        except TypeError:
            raise ValueError("Параметры должны быть преобразуемы в numpy массив") from None

    def _get_mse_values(self):
        translation_noises = np.random.normal(loc=0, scale=self.mse_translation)
        rotation_angles_noises = np.random.normal(loc=0, scale=self.mse_rotation_angles)
        translation = self.base_translation + translation_noises
        rotation_angles = self.base_rotation_angles + rotation_angles_noises
        return rotation_angles, translation

    @staticmethod
    def _get_rotation_matrix(rotation_angles: np.ndarray) -> np.ndarray:
        rx, ry, rz = np.radians(rotation_angles)
        cos_x, sin_x = np.cos(rx), np.sin(rx)
        cos_y, sin_y = np.cos(ry), np.sin(ry)
        cos_z, sin_z = np.cos(rz), np.sin(rz)
        rotation_matrix_x = np.array([
            [1, 0, 0],
            [0, cos_x, -sin_x],
            [0, sin_x, cos_x]
        ])
        rotation_matrix_y = np.array([
            [cos_y, 0, sin_y],
            [0, 1, 0],
            [-sin_y, 0, cos_y]
        ])
        rotation_matrix_z = np.array([
            [cos_z, -sin_z, 0],
            [sin_z, cos_z, 0],
            [0, 0, 1]
        ])
        return rotation_matrix_z @ rotation_matrix_y @ rotation_matrix_x

    def calculate_orientation_mse_location(
            self,
            ray_origins: np.ndarray,
            locations: np.ndarray,
            index_rays: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        if len(locations) == 0:
            return np.empty((0, 3)), np.empty((0, 3))
        rotation_angles, translation = self._get_mse_values()
        corresponding_origins = ray_origins[index_rays]
        rotation_matrix = self._get_rotation_matrix(rotation_angles)
        rotated_locations = (locations - corresponding_origins) @ rotation_matrix.T + corresponding_origins
        transformed_locations = rotated_locations + translation
        transformed_origins = ray_origins + translation
        return transformed_origins, transformed_locations
