import trimesh
from sklearn.neighbors import NearestNeighbors

from app.mesh.MeshIterator import MeshIterator
from app.mesh.mesh_triangulators.ScipyTriangulator import ScipyTriangulator
from app.scan.ScanPoint import ScanPoint


class Mesh:

    def __init__(self):
        self.mesh = None
        self.vertices_colors = None
        self.face_colors = None

    def __iter__(self):
        return iter(self.mesh.faces)

    def __iter__(self):
        return iter(MeshIterator(self))

    def __len__(self):
        return len(self.mesh.faces)

    def create_mesh_from_scan(self, scan, scan_triangulator=ScipyTriangulator):
        scan_triangulator().create_mesh(mesh=self, scan=scan)
        return self

    def load_mesh_from_file(self, filepath):
        self.mesh = trimesh.load(filepath)
        return self

    def simplify_mesh(self, face_count=None, target_reduction=None, save_colors=True):
        if face_count is not None:
            simplified = self.mesh.simplify_quadric_decimation(face_count=face_count)
        elif target_reduction is not None:
            simplified = self.mesh.simplify_quadric_decimation(percent=target_reduction)
        else:
            raise ValueError("Нет параметров для разрежения")
        if save_colors:
            nn = NearestNeighbors(n_neighbors=1).fit(self.mesh.vertices)
            _, indices = nn.kneighbors(simplified.vertices)
            # Переносим цвета
            simplified.visual.vertex_colors = self.mesh.visual.vertex_colors[indices.flatten()]
        self.mesh = simplified

    def export_mesh(self, filepath):
        self.mesh.export(filepath)

    def plot(self):
        self.mesh.show()


if __name__ == "__main__":
    from app.scan.Scan import Scan
    scan = Scan("Scan1")
    print(scan)
    scan.import_points_from_file(file_path=r"../../src/PCLD_1.las")
    mesh = Mesh().create_mesh_from_scan(scan=scan)
    print(mesh)
    print(len(mesh))
    # mesh.plot()
    mesh.simplify_mesh(face_count=1000)
    mesh.plot()
    print(len(mesh))
    for t in mesh:
        print(t)
    # mesh.export_mesh("./mesh.ply")
