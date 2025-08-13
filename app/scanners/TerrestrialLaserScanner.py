import numpy as np

from CONFIG import RANDOM_SEED
from app.scanners.ScannerABC import ScannerABC


class TerrestrialLaserScanner(ScannerABC):

    def __init__(self, name,
                 horizontal_limits,
                 vertical_limits,
                 max_range,
                 angular_accuracy,
                 distance_accuracy=0.,
                 random_seed=RANDOM_SEED,
                 ):
        super().__init__(random_seed=random_seed)
        self.name = name
        self.horizontal_limits = horizontal_limits
        self.vertical_limits = vertical_limits
        self.max_range = max_range
        self.angular_accuracy = angular_accuracy
        self.distance_accuracy = distance_accuracy

    @staticmethod
    def _generate_directions_2d(start_angle, end_angle, step_angle):
        start_angle, end_angle, step_angle = [float(elm) for elm in (start_angle, end_angle, step_angle)]
        if np.isclose(step_angle, 0):
            raise ValueError("Угловой шаг не может быть нулевым")

        if start_angle <= end_angle:
            angles = np.arange(start_angle, end_angle, step_angle)
        else:
            angles = np.arange(start_angle, end_angle, -step_angle)
        return angles

    def _get_mse_directions(self, base_directions):
        # Создаем копию для результата
        mse_directions = base_directions.copy()
        # Находим уникальные зенитные углы и их индексы
        zenith_values, zenith_indices = np.unique(base_directions[:, 0], return_inverse=True)
        # Генерируем азимутальный шум - по одному значению на каждый зенитный ряд
        azimuth_noises = np.random.normal(0, self.angular_accuracy, size=len(zenith_values))
        # Генерируем зенитный шум - индивидуальный для каждого направления
        zenith_noises = np.random.normal(0, self.angular_accuracy, size=len(base_directions))
        # Применяем шумы
        mse_directions[:, 0] += azimuth_noises[zenith_indices]
        mse_directions[:, 1] += zenith_noises
        # Нормализуем углы
        mse_directions[:, 0] = np.mod(mse_directions[:, 0], 360)
        mse_directions[:, 1] = np.clip(mse_directions[:, 1], self.vertical_limits[0],
                                       self.vertical_limits[1])
        return mse_directions

    def get_scanner_directions(self, azimuth_step, zenith_step=None):
        super().get_scanner_directions()
        zenith_step = zenith_step if zenith_step is not None else azimuth_step
        zenith_angles = self._generate_directions_2d(self.vertical_limits[0],
                                                     self.vertical_limits[1],
                                                     zenith_step)
        azimuth_angles = self._generate_directions_2d(self.horizontal_limits[0],
                                                      self.horizontal_limits[1],
                                                      azimuth_step)
        # Создаем сетку углов (внешнее произведение)
        azimuth_grid, zenith_grid = np.meshgrid(azimuth_angles, zenith_angles)
        # Объединяем в массив (N, 2)
        base_directions = np.column_stack((azimuth_grid.ravel(), zenith_grid.ravel()))
        mse_directions = self._get_mse_directions(base_directions)
        return base_directions, mse_directions


if __name__ == "__main__":
    import time
    scanner = TerrestrialLaserScanner("Test", horizontal_limits=(0, 360),
                                      vertical_limits=(60, 120),
                                      max_range=1000,
                                      # angular_accuracy=0.0028,
                                      angular_accuracy=1,
                                      )
    print(time.time())
    base_directions, mse_directions = scanner.get_scanner_directions(30.)
    print("!")
    print(time.time())
    print(len(base_directions))
    print(len(mse_directions))

    for idx in range(len(base_directions)):
        print(base_directions[idx], "\t\t\t\t", mse_directions[idx])
