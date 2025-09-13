from endpoint_configs.config_model import EndpointConfig
from extraction_configs.registry import get_extraction_config
from extraction_configs.schema import ExtractionConfig
from extraction_handler.lang_graph.lang_graph import GraphExtractionHandler
from tool_handler.base import ToolHandler


class ToolBuilder:
    def __init__(self, endpoint_configs: list[EndpointConfig]):
        self.endpoint_configs = endpoint_configs

    def create_tool_handlers(self):
        tool_handlers = []
        for cfg in self.endpoint_configs:
            extraction_config = get_extraction_config(cfg.name)
            extraction_handler_cls = GraphExtractionHandler
            handler = ToolHandler(cfg, extraction_config, extraction_handler_cls)
            tool_handlers.append(handler)
        return tool_handlers