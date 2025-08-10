from app.scan.ScanPoint import ScanPoint
from app.scan.parsers.ScanParserABC import ScanParserABC


class ScanParserFormTxtWithoutColor(ScanParserABC):
    def parse(self, scan, default_color=(0, 0, 0)):
        with open(self.file_path, "rt", encoding="UTF-8") as file:
            for line in file:
                line = line.strip().split()
                xyz = [float(xyz_) for xyz_ in line[:3]]
                rgb = default_color
                point = ScanPoint(x=xyz[0], y=xyz[1], z=xyz[2], color=rgb)
                scan.add_point(point)
