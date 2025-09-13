from endpoint_configs.config_model import EndpointConfig
from extraction_configs.schema import ExtractionConfig
from extractor_factory.base import ExtractorFactory
from parameter_extraction.parameter_extraction import ParameterExtraction
from abc import ABC, abstractmethod

from parameters.parameter import Parameter


class ExtractionHandler(ABC):
    def __init__(self, endpoint_config: EndpointConfig, extraction_config: ExtractionConfig):
        self.endpoint_config = endpoint_config
        self.extraction_config = extraction_config
        self.extractor_factory = ExtractorFactory(extraction_config)

    @abstractmethod
    async def extract_parameters(self, parameters: list[Parameter], given_extractions: list[ParameterExtraction]) -> \
            list[ParameterExtraction]:
        pass
