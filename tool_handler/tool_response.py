from typing import Literal, Optional

from pydantic import BaseModel, HttpUrl, Field


class Explanations(BaseModel):
    segments: list[str]


class HttpRequest(BaseModel):
    url: HttpUrl
    method: Literal['GET', 'POST', 'PUT', 'DELETE']
    params: dict[str, str] = Field(default_factory=dict)
    headers: dict[str, str]
    body: Optional[str] = None


class ToolResponse(BaseModel):
    http_request: HttpRequest
    extractions: BaseModel
    explanations: Optional[Explanations] = None
