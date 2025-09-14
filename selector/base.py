from abc import ABC, abstractmethod

from endpoint_configs.config_model import EndpointConfig
from extraction_configs.schema import ExtractionConfig
from parameters.parameter import Parameter


class ParameterSelector(ABC):
    def __init__(self, endpoint_config: EndpointConfig, extraction_config: ExtractionConfig):
        self.endpoint_config = endpoint_config
        self.extraction_config = extraction_config

    async def select_parameters(self, query: str, parameters: list[Parameter]):
        candidate_parameters = [p for p in parameters if p.name in self.extraction_config.filterable_parameters_names]
        selected_parameters = [p for p in parameters if p not in candidate_parameters]
        relevant_parameters = await self.find_relevant_parameters(query, candidate_parameters)
        return selected_parameters + relevant_parameters

    @abstractmethod
    async def find_relevant_parameters(self, query: str, candidate_parameters: list[Parameter]) -> list[Parameter]:
        pass
