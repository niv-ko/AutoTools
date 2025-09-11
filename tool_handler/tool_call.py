from typing import Annotated, Optional

from pydantic import BaseModel, Field

from tool_handler.consts import QUERY_FIELD_DESCRIPTION, PARAMETERS_TO_EXTRACT_FIELD_DESCRIPTION


class ToolCall(BaseModel):
    query: Annotated[str, Field(..., description=QUERY_FIELD_DESCRIPTION)]
    parameters_to_extract: Annotated[Optional[list[str]], Field(
        default=None, description=PARAMETERS_TO_EXTRACT_FIELD_DESCRIPTION)]
