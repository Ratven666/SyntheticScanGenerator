from app.scan_genetator.vectors_generator.TLSVectorGenerator import TLSVectorGenerator
from app.scan_genetator.vectors_generator.VectorGeneratorABC import VectorGeneratorABC
from app.scanners.TerrestrialLaserScanner import TerrestrialLaserScanner


class VectorGeneratorFactory(VectorGeneratorABC):

    def __init__(self, *position_data, **kw_position_data):
        self.position_data = position_data
        self.kw_position_data = kw_position_data

    def _get_custom_vector_generator_by_scanner_class(self, scanner):
        if isinstance(scanner, TerrestrialLaserScanner):
            return TLSVectorGenerator(*self.position_data, **self.kw_position_data)

    def get_vectors(self, scanner, *scan_parameters, **kw_scan_parameters):
        vector_generator = self._get_custom_vector_generator_by_scanner_class(scanner)
        return vector_generator.get_vectors(scanner, *scan_parameters, **kw_scan_parameters)
