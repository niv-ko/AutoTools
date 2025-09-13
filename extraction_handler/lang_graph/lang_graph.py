from endpoint_configs.config_model import EndpointConfig
from extraction_configs.schema import ExtractionConfig
from extraction_handler.base import ExtractionHandler
from extraction_handler.lang_graph.graph_manager import LangGraphManager
from parameter_extraction.parameter_extraction import ParameterExtraction
from parameters.parameter import Parameter


class GraphExtractionHandler(ExtractionHandler):

    def __init__(self, endpoint_config: EndpointConfig, extraction_config: ExtractionConfig):
        super().__init__(endpoint_config, extraction_config)
        self.graph_manager = LangGraphManager(endpoint_config, extraction_config, self.extractor_factory)
        self.graph = self.graph_manager.create_graph()

    async def extract_parameters(self, parameters: list[Parameter], given_extractions: list[ParameterExtraction]) -> \
            list[ParameterExtraction]:
        return await self.graph_manager.run_graph(self.graph, parameters, given_extractions)


        