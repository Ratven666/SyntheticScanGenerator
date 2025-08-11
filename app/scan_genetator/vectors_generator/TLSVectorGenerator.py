import numpy as np

from app.base.Point import Point
from app.scan_genetator.vectors_generator.VectorGeneratorABC import VectorGeneratorABC
from app.scanners.TerrestrialLaserScanner import TerrestrialLaserScanner


class TLSVectorGenerator(VectorGeneratorABC):

    def __init__(self, center_point: Point):
        self.center_point = center_point

    @classmethod
    def init_by_xy_on_mesh(cls, x, y, mesh, hi=1.5):
        z = mesh.get_z_by_xy(x, y)
        if z is None:
            raise ValueError("Точка лежит за пределами поверхности!")
        center_point = Point(x=x,
                             y=y,
                             z=z+hi)
        return cls(center_point=center_point)

    @staticmethod
    def _directions_to_vectors_np(directions):
        """
        Векторизованное преобразование углов в единичные векторы
        Параметры:
        directions - массив NumPy формы (N, 2), где каждая строка - (азимут, зенит)
        Возвращает:
        Массив NumPy формы (N, 3) с единичными векторами
        """
        azimuth_rad = np.deg2rad(directions[:, 0])
        zenith_rad = np.deg2rad(directions[:, 1])
        sin_zenith = np.sin(zenith_rad)
        x = sin_zenith * np.cos(azimuth_rad)
        y = sin_zenith * np.sin(azimuth_rad)
        z = np.cos(zenith_rad)
        return np.column_stack((x, y, z))

    def get_vectors(self, scanner, *scan_parameters, **kw_scan_parameters):
        base_directions, mse_directions = scanner.get_scanner_directions(*scan_parameters,
                                                                         **kw_scan_parameters)
        ray_origins = np.array([[self.center_point.x,
                                 self.center_point.y,
                                 self.center_point.z]] * len(base_directions))
        base_directions_vectors = self._directions_to_vectors_np(base_directions)
        mse_directions_vectors = self._directions_to_vectors_np(mse_directions)
        return ray_origins, base_directions, base_directions_vectors, mse_directions_vectors


if __name__ == "__main__":
    import time
    scanner = TerrestrialLaserScanner("Test", horizontal_limits=(0, 360),
                                      vertical_limits=(60, 120),
                                      max_range=1000,
                                      # angular_accuracy=0.0028,
                                      angular_accuracy=1,
                                      )
    tls_vg = TLSVectorGenerator(Point(100, 100, 100))
    ray_origins, base_directions, base_directions_vectors, mse_directions_vectors = tls_vg.get_vectors(scanner, azimuth_step=10,
                                                                                      zenith_step=10)

    for idx in range(len(ray_origins)):
        print(ray_origins[idx], "\t\t", base_directions_vectors[idx], "\t\t", mse_directions_vectors[idx])
