from endpoint_configs.schema import EndpointConfig
from extraction_configs.registry import get_extraction_config
from extraction_configs.schema import ExtractionConfig
from tool_handler.tool_handler import ToolHandler


class ToolBuilder:
    def __init__(self, endpoint_configs: list[EndpointConfig]):
        self.endpoint_configs = endpoint_configs

    def create_tool_handlers(self):
        tool_handlers = []
        for cfg in self.endpoint_configs:
            extraction_config = get_extraction_config(cfg.name)
            handler = ToolHandler(cfg, extraction_config)
            tool_handlers.append(handler)
        return tool_handlers