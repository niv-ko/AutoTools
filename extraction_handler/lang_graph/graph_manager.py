from operator import add
from typing import Callable, Annotated, TypeVar, Optional

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.runtime import Runtime
from pydantic import BaseModel

from endpoint_configs.config_model import EndpointConfig
from extraction_configs.schema import ExtractionConfig
from extractor_factory.base import ExtractorFactory
from extractors.base import Extractor
from parameter_extraction.parameter_extraction import ParameterExtraction
from parameters.parameter import Parameter
from selector.base import ParameterSelector

T = TypeVar('T')


class LangGraphManager:
    def __init__(self, endpoint_config: EndpointConfig, extraction_config: ExtractionConfig,
                 extractor_factory: ExtractorFactory):
        self.endpoint_config = endpoint_config
        self.extraction_config = extraction_config
        self.extractor_factory = extractor_factory

    async def get_parameters_to_extract(self, requested: list[Parameter]) -> list[Parameter]:
        params_to_extract: list[Parameter] = list()
        stack = list(requested)
        while stack:
            p = stack.pop()
            if p in params_to_extract:
                continue
            params_to_extract.append(p)
            requirements = self.extraction_config.get_required_parameters(p.name)
            stack.extend([self.endpoint_config.get_param_by_name(req) for req in requirements])
        return params_to_extract

    class State(BaseModel):
        extractions: Annotated[list[ParameterExtraction], add]

        def is_extracted(self, parameter: Parameter) -> bool:
            return any(pe.parameter.name == parameter.name for pe in self.extractions)

    class Context(BaseModel):
        query: str
        parameters_to_extract: list[Parameter]

    def make_extraction_node(self, parameter: Parameter, extractor: Extractor):
        async def _node(state: LangGraphManager.State, runtime: Runtime[LangGraphManager.Context]):
            if parameter not in runtime.context.parameters_to_extract or state.is_extracted(parameter):
                return {}
            required_extractions = [e for e in state.extractions if e.parameter.name in
                                    self.extraction_config.get_required_parameters(parameter.name)]
            value = await extractor(runtime.context.query, required_extractions)
            return {"extractions": [ParameterExtraction[parameter.param_type()](parameter=parameter, result=value)]}

        _node.__name__ = f"{parameter.name}_extractor_node"
        return _node

    def create_graph(self) -> CompiledStateGraph:
        g = StateGraph(state_schema=LangGraphManager.State, context_schema=LangGraphManager.Context)

        for parameter in self.endpoint_config.parameters:
            extractor = self.extractor_factory.get_extractor(parameter)
            node = self.make_extraction_node(parameter, extractor)
            g.add_node(parameter.name, node)

        sink_nodes = {p.name for p in self.endpoint_config.parameters}

        for parameter in self.endpoint_config.parameters:
            requirements = self.extraction_config.get_required_parameters(parameter.name)
            if requirements:
                g.add_edge(requirements, parameter.name)
                sink_nodes = sink_nodes.difference(requirements)
            else:
                g.add_edge(START, parameter.name)

        g.add_edge(list(sink_nodes), END)

        return g.compile()

    async def run_graph(self, query: str, graph: CompiledStateGraph, requested: list[Parameter],
                        given_extractions: list[ParameterExtraction]) \
            -> list[ParameterExtraction]:
        parameters_to_extract = await self.get_parameters_to_extract(requested)
        context = LangGraphManager.Context(query=query, parameters_to_extract=parameters_to_extract)
        initial_state = LangGraphManager.State(extractions=given_extractions)
        state_dict = await graph.ainvoke(initial_state, context=context)
        final_state = LangGraphManager.State.model_validate(state_dict)
        return final_state.extractions
