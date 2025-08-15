from app.scan_genetator.points_filters.PointsFilterABC import PointsFilterABC


class FalsePointsFilters(PointsFilterABC):
    def _filter_logic(self, point_index):
        return True
