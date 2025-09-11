from extractors.base import Extractor
from parameters.parameter import Parameter
from extractors import registry


class ExtractorFactory:
    def __init__(self, extraction_config):
        self.extraction_config = extraction_config

    def get_extractor(self, parameter: Parameter) -> Extractor:
        return registry.get_extractor(self.extraction_config.extraction_method, parameter)
