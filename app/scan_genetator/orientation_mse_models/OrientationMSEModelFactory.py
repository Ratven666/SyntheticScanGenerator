from app.scan_genetator.orientation_mse_models.FalseOrientationMSEModel import FalseOrientationMSEModel
from app.scan_genetator.orientation_mse_models.OrientationMSEModelABC import OrientationMSEModelABC
from app.scan_genetator.orientation_mse_models.TLSOrientationMSEModel import TLSOrientationMSEModel
from app.scanners.TerrestrialLaserScanner import TerrestrialLaserScanner


class OrientationMSEModelFactory(OrientationMSEModelABC):

    def get_custom_orientation_mse_model_class(self):
        if self.orientation_mse_parameters_diсt is None:
            return FalseOrientationMSEModel
        elif isinstance(self.scanner, TerrestrialLaserScanner):
            return TLSOrientationMSEModel

    def calculate_orientation_mse_location(self, ray_origins, locations, index_rays):
        orientation_mse_model = self.get_custom_orientation_mse_model_class()(self.scanner,
                                                                              self.orientation_mse_parameters_diсt)
        return orientation_mse_model.calculate_orientation_mse_location(ray_origins, locations, index_rays)
