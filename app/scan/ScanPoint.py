from app.base.Point import Point


class ScanPoint(Point):

    def __init__(self, x, y, z, color=(0, 0, 0)):
        super().__init__(x, y, z)
        self.color = color

    def __str__(self):
        return f"ScanPoint (x={self.x:.3f}, y={self.y:.3f}, z={self.z:.3f}, color={self.color})"

    def __repr__(self):
        return f"SP=[xyz=({self.x:.3f}, {self.y:.3f}, {self.z:.3f})])"
