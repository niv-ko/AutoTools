import re
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

from pydantic import create_model

from consts import TOOL_CALL_MODEL_NAME_PREFIX, SUPPORTED_PARAMETERS_FIELD_NAME
from endpoint_configs.schema import EndpointConfig
from extraction_configs.schema import ExtractionConfig
from extraction_handler.base import ExtractionHandler
from tool_handler.tool_call import ToolCall
from tool_handler.tool_response import ToolResponse

ToolCallType = TypeVar("ToolCallType", bound=ToolCall)


class ToolHandler(ABC, Generic[ToolCallType]):
    def __init__(self, endpoint_config: EndpointConfig, extraction_config: ExtractionConfig):
        self.endpoint_config = endpoint_config
        self.extraction_config = extraction_config
        self.extraction_handler: ExtractionHandler = None

    @abstractmethod
    def handle_call(self, tool_call: ToolCallType) -> ToolResponse:
        parameters_names_to_extract = tool_call.parameters_to_extract

        parameters_to_extract = self.endpoint_config.get_params_by_names(parameters_names_to_extract)
        self.extraction_handler.extract_parameters()

    def create_tool_call(self) -> Type[ToolCallType]:
        fields = {SUPPORTED_PARAMETERS_FIELD_NAME: self.endpoint_config.endpoint_schema()}

        model_name = f"{TOOL_CALL_MODEL_NAME_PREFIX}{self.endpoint_config.name}"

        model = create_model(
            model_name,
            __config__=None,
            __base__=ToolCall,
            __module__=__name__,
            **fields,
        )

        return model  # type: ignore
