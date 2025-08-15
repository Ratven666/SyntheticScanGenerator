from abc import ABC, abstractmethod

import numpy as np

from app.scan_genetator.real_location_calculator.RLCUtilModelsClass import RLCUtilModelsClass


class PointsFilterABC(ABC, RLCUtilModelsClass):

    @abstractmethod
    def _filter_logic(self, point_index):
        pass

    def get_points_mask(self,
                        real_distance_calculator_obj,
                        ):
        self._init_model_data(real_distance_calculator_obj=real_distance_calculator_obj)

        vectorized_filter = np.vectorize(self._filter_logic)
        mask = vectorized_filter(point_index=range(len(self.locations)))
        return mask
