from pydantic import BaseModel


class ToolCall(BaseModel):
    query: str
