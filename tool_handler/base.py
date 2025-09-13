import re
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

from pydantic import create_model, BaseModel

from consts import TOOL_CALL_MODEL_NAME_PREFIX, SUPPORTED_PARAMETERS_FIELD_NAME
from endpoint_configs.config_model import EndpointConfig
from endpoint_configs.schema import EndpointSchema
from extraction_configs.schema import ExtractionConfig
from extraction_handler.base import ExtractionHandler
from parameter_extraction.parameter_extraction import ParameterExtraction
from request_generator.base import RequestGenerator
from tool_handler.tool_call import ToolCall
from tool_handler.tool_response import ToolResponse

S = TypeVar("S", bound=EndpointSchema)
T = TypeVar("T", bound=EndpointSchema)


class ToolHandler(ABC, Generic[S, T]):
    def __init__(self, endpoint_config: EndpointConfig[S, T], extraction_config: ExtractionConfig,
                 extraction_handler_cls: Type[ExtractionHandler], request_generator_cls: Type[RequestGenerator],
                 ):
        self.endpoint_config = endpoint_config
        self.extraction_config = extraction_config
        self.extraction_handler: ExtractionHandler = extraction_handler_cls(endpoint_config, extraction_config)
        self.request_generator: RequestGenerator[T] = request_generator_cls[T]()

    @abstractmethod
    async def handle_call(self, tool_call: ToolCall[S]) -> ToolResponse[T]:
        parameters_names_to_extract = tool_call.parameters_to_extract
        parameters_to_extract = self.endpoint_config.get_params_by_names(parameters_names_to_extract)
        input_values_model = tool_call.supported_parameters
        given_extractions = list()
        for param_name, v in input_values_model.model_dump(exclude_unset=True).items():
            param = self.endpoint_config.get_param_by_name(param_name)
            given_extractions.append(ParameterExtraction(parameter=param, value=v))

        extractions = await self.extraction_handler.extract_parameters(parameters_to_extract, given_extractions)
        endpoint_output_schema = self.endpoint_config.endpoint_output_schema.from_extractions(extractions)
        http_request = self.request_generator.generate_request(endpoint_output_schema)
        return ToolResponse(extractions=endpoint_output_schema, http_request=http_request)


