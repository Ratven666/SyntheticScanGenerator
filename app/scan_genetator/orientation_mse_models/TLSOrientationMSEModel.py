import numpy as np
from typing import Tuple

from app.scan_genetator.orientation_mse_models.OrientationMSEModelABC import OrientationMSEModelABC


class TLSOrientationMSEModel(OrientationMSEModelABC):

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
        try:
            translation = np.asarray(self.orientation_mse_parameters_diсt["translation"], dtype=np.float64)
            rotation_angles = np.asarray(self.orientation_mse_parameters_diсt["rotation_angles"], dtype=np.float64)
        except KeyError as e:
            raise ValueError(f"Отсутствует обязательный параметр: {e}") from None
        except TypeError:
            raise ValueError("Параметры должны быть преобразуемы в numpy массив") from None
        if len(locations) == 0:
            return np.empty((0, 3)), np.empty((0, 3))
        corresponding_origins = ray_origins[index_rays]
        rotation_matrix = self._get_rotation_matrix(rotation_angles)
        rotated_locations = (locations - corresponding_origins) @ rotation_matrix.T + corresponding_origins
        transformed_locations = rotated_locations + translation
        transformed_origins = ray_origins + translation
        return transformed_origins, transformed_locations
