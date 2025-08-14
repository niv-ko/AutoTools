import re
from typing import TypeVar, Generic, Type

from endpoint_configs.base import EndpointConfig
from extraction_configs.schema import ExtractionConfig

from pydantic import create_model, Field
from tool_handler.tool_call import ToolCall

ToolCallType = TypeVar("ToolCallType", bound=ToolCall)


class ToolHandler(Generic[ToolCallType]):
    def __init__(self, endpoint_config: EndpointConfig, extraction_config: ExtractionConfig):
        self.endpoint_config = endpoint_config
        self.extraction_config = extraction_config
        self.extraction_handler = None

    def handle_call(self, tool_call: ToolCallType):
        pass

    def create_tool_call(self) -> Type[ToolCallType]:
        fields = {
            "query": (str, Field(..., description="The user query")),
        }

        for p in self.endpoint_config.parameters:
            field_name = _sanitize(p.name)
            fields[field_name] = (
                p.annotation,
                Field(
                    default=None,
                    description=p.description,
                    alias=p.name,  # accept original name in input/output
                ),
            )

        model_name = f"ToolCall_{self.endpoint_config.name}"

        model = create_model(  # type: ignore
            model_name,
            __config__=None,
            __base__=ToolCall,
            __module__=__name__,
            **fields,
        )

        return model  # type: ignore


def _sanitize(name: str) -> str:
    # valid Python identifier; keep alias for the original name
    name2 = re.sub(r'\W|^(?=\d)', '_', name)
    if name2 == "":
        name2 = "_"
    return name2
