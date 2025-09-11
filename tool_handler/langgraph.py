from endpoint_configs.schema import EndpointConfig
from extraction_configs.schema import ExtractionConfig
from extraction_handler.lang_graph.lang_graph import GraphExtractionHandler
from tool_handler.base import ToolHandler, ToolCallType
from tool_handler.tool_response import ToolResponse


class LGToolHandler(ToolHandler):
    def __init__(self, endpoint_config: EndpointConfig, extraction_config: ExtractionConfig):
        super().__init__(endpoint_config, extraction_config)
        self.extraction_handler = GraphExtractionHandler(endpoint_config, extraction_config)
    def handle_call(self, tool_call: ToolCallType) -> ToolResponse:
