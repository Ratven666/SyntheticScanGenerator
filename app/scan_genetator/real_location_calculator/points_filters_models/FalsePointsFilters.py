from app.scan_genetator.real_location_calculator.points_filters_models.PointsFilterModelABC import PointsFilterABC


class FalsePointsFilters(PointsFilterABC):

    def _filter_logic(self, point_index):
        return True
