from typing import TypeVar, Generic, Type, Optional

from endpoint_configs.config_model import EndpointConfig
from endpoint_configs.schema import EndpointSchema
from extraction_configs.schema import ExtractionConfig
from extraction_handler.base import ExtractionHandler
from parameter_extraction.parameter_extraction import ParameterExtraction
from parameters.parameter import Parameter
from request_generator.base import RequestGenerator
from response_explainer.base import ResponseExplainer
from selector.base import ParameterSelector
from tool_handler.tool_call import ToolCall
from tool_handler.tool_response import ToolResponse

S = TypeVar("S", bound=EndpointSchema)
T = TypeVar("T", bound=EndpointSchema)


class ToolHandler(Generic[S, T]):
    def __init__(self, endpoint_config: EndpointConfig[S, T], extraction_config: ExtractionConfig,
                 extraction_handler_cls: Type[ExtractionHandler], request_generator_cls: Type[RequestGenerator],
                 selector: Optional[ParameterSelector], explainer: Optional[ResponseExplainer] = None,
                 ):
        self.endpoint_config = endpoint_config
        self.extraction_config = extraction_config
        self.extraction_handler = extraction_handler_cls(endpoint_config, extraction_config)
        self.request_generator = request_generator_cls[S, T](endpoint_config)
        self.selector = selector
        self.explainer = explainer

    async def handle_call(self, tool_call: ToolCall[S]) -> ToolResponse[T]:
        parameters_to_extract = self.get_parameters_to_extract(tool_call)
        given_extractions = self.get_given_extractions(tool_call)

        extractions = await self.extraction_handler.extract_parameters(parameters_to_extract, given_extractions)
        endpoint_output_schema = self.endpoint_config.endpoint_output_schema.from_extractions(extractions)
        http_request = self.request_generator.generate_request(endpoint_output_schema)
        return ToolResponse(extractions=endpoint_output_schema, http_request=http_request)

    def get_given_extractions(self, tool_call: ToolCall[S]) -> list[ParameterExtraction]:
        input_values_model = tool_call.supported_parameters
        given_extractions = list()
        if input_values_model is not None:
            for param_name, v in input_values_model.model_dump(exclude_unset=True).items():
                param = self.endpoint_config.get_param_by_name(param_name)
                given_extractions.append(ParameterExtraction(parameter=param, result=v))
        return given_extractions

    def get_parameters_to_extract(self, tool_call: ToolCall[S]) -> list[Parameter]:
        parameters_names_to_extract = tool_call.parameters_to_extract
        parameters_to_extract = self.endpoint_config.parameters if parameters_names_to_extract is None \
            else self.endpoint_config.get_params_by_names(parameters_names_to_extract)
        if self.selector is not None:
            parameters_to_extract = self.selector.select_parameters(tool_call.query, parameters_to_extract)
        return parameters_to_extract
