from typing import Annotated, Optional, TypeVar, Generic

from pydantic import BaseModel, Field, ConfigDict

from tool_handler.consts import QUERY_FIELD_DESCRIPTION, PARAMETERS_TO_EXTRACT_FIELD_DESCRIPTION

S = TypeVar("S", bound=BaseModel)


# add config
class ToolCall(BaseModel, Generic[S]):
    model_config = ConfigDict(extra="forbid")

    query: Annotated[str, Field(..., description=QUERY_FIELD_DESCRIPTION)]
    parameters_to_extract: Annotated[Optional[list[str]], Field(
        default=None, description=PARAMETERS_TO_EXTRACT_FIELD_DESCRIPTION)]
    supported_parameters: S
