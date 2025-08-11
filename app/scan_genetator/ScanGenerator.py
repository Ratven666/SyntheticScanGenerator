import numpy as np
import trimesh

from app.base.Point import Point
from app.mesh.Mesh import Mesh
from app.scan.Scan import Scan
from app.scan.ScanPoint import ScanPoint
from app.scan_genetator.vectors_generator.TLSVectorGenerator import TLSVectorGenerator
from app.scanners.ScannerABC import ScannerABC
from app.scanners.TerrestrialLaserScanner import TerrestrialLaserScanner


class ScanGenerator:

    def __init__(self, scanner: ScannerABC,
                 mesh: Mesh,
                 scan_parameters,
                 position_data,
                 distance_mse_model=None
                 ):
        self.scanner = scanner
        self.mesh = mesh
        self.scan_parameters = scan_parameters
        self.position_data = position_data
        self.distance_mse_model = distance_mse_model

    def _get_rays(self):
        vector_generator = TLSVectorGenerator(self.position_data)
        if isinstance(self.scan_parameters, tuple):
            r_origin, base_dir, b_dir_vec, mse_dir_vec = vector_generator.get_vectors(self.scanner,
                                                                            *self.scan_parameters)
        else:
            r_origin, base_dir, b_dir_vec, mse_dir_vec = vector_generator.get_vectors(self.scanner,
                                                                            **self.scan_parameters)
        return base_dir, r_origin, b_dir_vec, mse_dir_vec

    def get_points_by_rtx(self, ray_origins, ray_directions, only_first_cross=True):
        locations, index_ray, index_tri = self.mesh.rtx_by_dirs(ray_origins, ray_directions)
        if len(locations) > 0 and only_first_cross:
            distances = np.linalg.norm(locations - ray_origins[index_ray], axis=1)
            print(distances)
            sorted_idx = np.lexsort((distances, index_ray))
            locations = locations[sorted_idx]
            index_ray = index_ray[sorted_idx]
            index_tri = index_tri[sorted_idx]
            _, first_hit_idx = np.unique(index_ray, return_index=True)
            locations, index_ray, index_tri = (locations[first_hit_idx],
                                               index_ray[first_hit_idx],
                                               index_tri[first_hit_idx])
        return locations, index_ray, index_tri

    def calk_mse_locations(self, base_direction, ray_origins, locations, index_ray):
        base_direction = base_direction[index_ray]
        ray_origins = ray_origins[index_ray]
        distances = np.linalg.norm(locations - ray_origins, axis=1)

        # distances = np.sqrt(np.sum((locations - ray_origins) ** 2, axis=1))
        distances_noises = np.random.normal(0, self.scanner.distance_accuracy, size=len(distances))
        print(distances)
        distances += distances_noises

        azimuth_rad = np.deg2rad(base_direction[:, 0])
        zenith_rad = np.deg2rad(base_direction[:, 1])
        sin_zenith = np.sin(zenith_rad)
        x = distances * sin_zenith * np.cos(azimuth_rad)
        y = distances * sin_zenith * np.sin(azimuth_rad)
        z = distances * np.cos(zenith_rad)
        mse_locations = ray_origins + np.column_stack((x, y, z))
        return mse_locations

    def create_scan(self, locations, index_ray, index_tri, get_true_scan, with_color=True, base_color=(0, 0, 0)):
        scan = Scan(f"Scan_by_{self.mesh.name}_{self.position_data}_{self.scan_parameters}_is_{get_true_scan}_scan")
        for idx in range(len(locations)):
            x, y, z = locations[idx]
            id_ = index_ray[idx]
            if with_color:
                color = self.mesh.face_colors[index_tri[idx]][:3]
            else:
                color = base_color
            point = ScanPoint(x=x, y=y, z=z,
                              color=color, id_=id_)
            scan.add_point(point)
        return scan

    def get_scan(self, get_true_scan=True):
        base_direction, ray_origins, base_directions_vectors, mse_directions_vectors = self._get_rays()
        print(len(ray_origins))
        if get_true_scan:
            locations, index_ray, index_tri = self.get_points_by_rtx(ray_origins, base_directions_vectors)
        else:
            locations, index_ray, index_tri = self.get_points_by_rtx(ray_origins, mse_directions_vectors)
            locations = self.calk_mse_locations(base_direction, ray_origins, locations, index_ray)
        scan = self.create_scan(locations, index_ray, index_tri, get_true_scan=get_true_scan)
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
    scanner = TerrestrialLaserScanner("Test", horizontal_limits=(0, 360),
                                      vertical_limits=(60, 120),
                                      max_range=1000,
                                      angular_accuracy=0.0028,
                                      distance_accuracy=0.005,
                                      )
    position_data = Point(6375, 12675, 112)
    # scan_parameters = {"azimuth_step": 10, "zenith_step": None}
    scan_parameters = 10, 10

    scan = Scan("").import_points_from_file(file_path=r"../../src/PCLD_1.las")
    mesh = Mesh().create_mesh_from_scan(scan=scan)
    mesh.simplify_mesh(face_count=1000)

    # mesh.plot()

    sg = ScanGenerator(scanner=scanner,
                       mesh=mesh,
                       position_data=position_data,
                       scan_parameters=scan_parameters,
                       )
    scan = sg.get_scan(get_true_scan=True)
    scan.export_points_from_file("true_scan.xyz")

    scan = sg.get_scan(get_true_scan=False)
    scan.export_points_from_file("mse_scan.xyz")

    # scan.plot()
    # for point in scan:
    #     print(point)
