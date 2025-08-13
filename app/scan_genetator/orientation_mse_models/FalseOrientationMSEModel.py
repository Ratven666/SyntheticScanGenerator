from app.scan_genetator.orientation_mse_models.OrientationMSEModelABC import OrientationMSEModelABC


class FalseOrientationMSEModel(OrientationMSEModelABC):

    def calculate_orientation_mse_location(self, ray_origins, locations, index_rays):
        return ray_origins, locations
