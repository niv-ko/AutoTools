from typing import TypeVar

from endpoint_configs.config_model import EndpointConfig
from endpoint_configs.schema import EndpointSchema
from extraction_configs.registry import get_extraction_config
from extraction_configs.schema import ExtractionConfig, ParameterExtractionMethod, ExtractionMethod, \
    ParameterRequirement
from extraction_handler.lang_graph.lang_graph import GraphExtractionHandler
from request_generator.impl.dummy import DummyRequestGenerator
from tool_handler.base import ToolHandler


class ToolBuilder:
    def __init__(self, endpoint_configs: list[EndpointConfig]):
        self.endpoint_configs = endpoint_configs

    def create_tool_handlers(self):
        tool_handlers = []
        for cfg in self.endpoint_configs:
            extraction_config = get_extraction_config(cfg.name)
            extraction_handler_cls = GraphExtractionHandler
            request_generator_cls = DummyRequestGenerator
            selector = None
            # handler = ToolHandler(cfg, extraction_config, extraction_handler_cls)

            handler = ToolHandler(
                endpoint_config=cfg,
                extraction_config=ExtractionConfig(
                    parameter_extraction_methods=[
                        ParameterExtractionMethod(
                            parameter_name='a',
                            extraction_method=ExtractionMethod(
                                extractor_name="dummy"
                            )
                        ),
                        ParameterExtractionMethod(
                            parameter_name='b',
                            extraction_method=ExtractionMethod(
                                extractor_name="dummy"
                            )
                        )
                    ],
                    parameters_requirements=[
                        ParameterRequirement(
                            parameter_name='b',
                            required_parameters_names=['a']
                        )
                    ]
                ),
                extraction_handler_cls=extraction_handler_cls,
                request_generator_cls=request_generator_cls,
                selector=selector
            )
            tool_handlers.append(handler)
        return tool_handlers
