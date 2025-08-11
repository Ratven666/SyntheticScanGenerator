import numpy as np

from CONFIG import DEFAULT_POINTS_COLOR, RTX_RAYS_CHUNK
from app.mesh.Mesh import Mesh
from app.scan.Scan import Scan
from app.scan.ScanPoint import ScanPoint
from app.scan_genetator.vectors_generator.VectorGeneratorFactory import VectorGeneratorFactory
from app.scanners.ScannerABC import ScannerABC


class ScanGenerator:

    def __init__(self,
                 scanner: ScannerABC,
                 mesh: Mesh,
                 scan_parameters,
                 position_data,
                 distance_mse_model=None,
                 ):
        self.scanner = scanner
        self.mesh = mesh
        self.scan_parameters = scan_parameters
        self.position_data = position_data
        self.distance_mse_model = distance_mse_model

    def _get_rays(self):
        vector_generator = VectorGeneratorFactory(self.position_data)
        if isinstance(self.scan_parameters, tuple):
            r_origin, base_dir, b_dir_vec, mse_dir_vec = vector_generator.get_vectors(self.scanner,
                                                                                      *self.scan_parameters)
        else:
            r_origin, base_dir, b_dir_vec, mse_dir_vec = vector_generator.get_vectors(self.scanner,
                                                                                      **self.scan_parameters)
        return base_dir, r_origin, b_dir_vec, mse_dir_vec

    @staticmethod
    def _get_first_points(ray_origins, locations, index_ray, index_tri):
        """Оставляет только первые пересечения для каждого луча"""
        if len(locations) == 0:
            return np.array([]), np.array([]), np.array([])
        # Вычисляем расстояния от начала лучей до точек пересечения
        distances = np.linalg.norm(locations - ray_origins[index_ray], axis=1)
        # Сортируем по индексу луча и расстоянию
        sorted_idx = np.lexsort((distances, index_ray))
        locations = locations[sorted_idx]
        index_ray = index_ray[sorted_idx]
        index_tri = index_tri[sorted_idx]
        # Оставляем только первое вхождение для каждого луча
        _, first_hit_idx = np.unique(index_ray, return_index=True)
        return locations[first_hit_idx], index_ray[first_hit_idx], index_tri[first_hit_idx]

    def _filter_point_by_max_range(self, ray_origins, locations, index_ray, index_tri):
        """Фильтрует точки по максимальному расстоянию"""
        if len(locations) == 0:
            return np.array([]), np.array([]), np.array([])
        distances = np.linalg.norm(locations - ray_origins[index_ray], axis=1)
        mask = distances < self.scanner.max_range
        return locations[mask], index_ray[mask], index_tri[mask]

    def _get_points_by_rtx(self, ray_origins, ray_directions, only_first_cross=True, chunk_size=RTX_RAYS_CHUNK):
        """
        Выполняет трассировку лучей с обработкой данных по частям
        Параметры:
            ray_origins: массив начальных точек лучей (N, 3)
            ray_directions: массив направлений лучей (N, 3)
            only_first_cross: оставлять только первые пересечения
            chunk_size: размер чанка для обработки
        Возвращает:
            Кортеж (locations, index_ray, index_tri)
        """
        if len(ray_origins) != len(ray_directions):
            raise ValueError("ray_origins и ray_directions должны иметь одинаковую длину")
        all_results = []
        print(len(ray_origins))
        # Обработка по чанкам
        for i in range(0, len(ray_origins), chunk_size):
            print(i)
            chunk_start = i
            chunk_end = min(i + chunk_size, len(ray_origins))
            chunk_origins = ray_origins[chunk_start:chunk_end]
            chunk_directions = ray_directions[chunk_start:chunk_end]
            # Выполняем трассировку для чанка
            loc, idx_ray, idx_tri = self.mesh.rtx_by_dirs(chunk_origins, chunk_directions)
            if len(loc) > 0:
                # Корректируем индексы лучей относительно общего массива
                idx_ray += chunk_start
                if only_first_cross:
                    loc, idx_ray, idx_tri = self._get_first_points(ray_origins, loc, idx_ray, idx_tri)
                loc, idx_ray, idx_tri = self._filter_point_by_max_range(ray_origins, loc, idx_ray, idx_tri)
                if len(loc) > 0:
                    all_results.append((loc, idx_ray, idx_tri))
        # Объединяем результаты
        if all_results:
            locations = np.concatenate([r[0] for r in all_results])
            index_ray = np.concatenate([r[1] for r in all_results])
            index_tri = np.concatenate([r[2] for r in all_results])
        else:
            locations, index_ray, index_tri = np.array([]), np.array([]), np.array([])
        return locations, index_ray, index_tri

    def _calk_mse_locations(self, base_direction, ray_origins, locations, index_ray):
        base_direction = base_direction[index_ray]
        ray_origins = ray_origins[index_ray]
        distances = np.linalg.norm(locations - ray_origins, axis=1)

        distances_noises = np.random.normal(0, self.scanner.distance_accuracy, size=len(distances))

        distances += distances_noises
        azimuth_rad = np.deg2rad(base_direction[:, 0])
        zenith_rad = np.deg2rad(base_direction[:, 1])
        sin_zenith = np.sin(zenith_rad)
        x = distances * sin_zenith * np.cos(azimuth_rad)
        y = distances * sin_zenith * np.sin(azimuth_rad)
        z = distances * np.cos(zenith_rad)
        mse_locations = ray_origins + np.column_stack((x, y, z))
        return mse_locations

    def _init_scan(self, locations, index_ray, index_tri, get_true_scan, with_color=True):
        scan = Scan(f"Scan_by_{self.mesh.name}_{self.position_data}_{self.scan_parameters}_is_{get_true_scan}_scan")
        for idx in range(len(locations)):
            x, y, z = locations[idx]
            id_ = index_ray[idx]
            if with_color:
                color = self.mesh.face_colors[index_tri[idx]][:3]
            else:
                color = DEFAULT_POINTS_COLOR
            point = ScanPoint(x=x, y=y, z=z,
                              color=color, id_=id_)
            scan.add_point(point)
        return scan

    def create_scan(self, get_true_scan=True):
        base_direction, ray_origins, base_directions_vectors, mse_directions_vectors = self._get_rays()
        if get_true_scan:
            locations, index_ray, index_tri = self._get_points_by_rtx(ray_origins, base_directions_vectors)
        else:
            locations, index_ray, index_tri = self._get_points_by_rtx(ray_origins, mse_directions_vectors)

            locations = self._calk_mse_locations(base_direction, ray_origins, locations, index_ray)
        scan = self._init_scan(locations, index_ray, index_tri, get_true_scan=get_true_scan)
        return scan
        # print(f"Найдено пересечений: {len(locations)}")
        # # Визуализация
        # if len(locations) > 0:
        #     scene = trimesh.Scene([
        #         self.mesh[0].mesh,
        #         trimesh.points.PointCloud(locations, colors=[255, 0, 0]),
        #     ])
        #     scene.show()


if __name__ == "__main__":
    from app.scanners.TerrestrialLaserScanner import TerrestrialLaserScanner
    from app.base.Point import Point

    scanner = TerrestrialLaserScanner("Test", horizontal_limits=(0, 360),
                                      vertical_limits=(60, 120),
                                      max_range=1000,
                                      angular_accuracy=0.0028,
                                      distance_accuracy=0.005,
                                      )
    position_data = Point(6375, 12675, 112)
    scan_parameters = {"azimuth_step": 1, "zenith_step": None}
    # scan_parameters = 10, 10

    scan = Scan("").import_points_from_file(file_path=r"../../src/PCLD_1.las")
    mesh = Mesh().create_mesh_from_scan(scan=scan)
    mesh.simplify_mesh(face_count=10_000)
    mesh.export_mesh("mesh.ply")

    # mesh.plot()

    sg = ScanGenerator(scanner=scanner,
                       mesh=mesh,
                       position_data=position_data,
                       scan_parameters=scan_parameters,
                       )
    scan = sg.create_scan(get_true_scan=True)
    scan.export_points_from_file("true_scan1.xyz")

    scan = sg.create_scan(get_true_scan=False)
    scan.export_points_from_file("mse_scan1.xyz")

    # scan.plot()
    # for point in scan:
    #     print(point)
