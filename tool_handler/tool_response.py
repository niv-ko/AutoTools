from typing import Literal, Optional, Generic, TypeVar

from pydantic import BaseModel, HttpUrl, Field

from endpoint_configs.schema import EndpointSchema

S = TypeVar("S", bound=EndpointSchema)

class Explanations(BaseModel):
    segments: list[str]


class HttpRequest(BaseModel):
    url: HttpUrl
    method: Literal['GET', 'POST', 'PUT', 'DELETE']
    params: dict[str, str] = Field(default_factory=dict)
    headers: dict[str, str] = Field(default_factory=dict)
    body: Optional[str] = None


class ToolResponse(BaseModel, Generic[S]):
    http_request: HttpRequest
    extractions: S
    explanations: Optional[Explanations] = None
