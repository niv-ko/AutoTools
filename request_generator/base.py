from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

from endpoint_configs.schema import EndpointSchema
from tool_handler.tool_response import HttpRequest

T = TypeVar("T", bound=EndpointSchema)


@abstractmethod
class RequestGenerator(ABC, Generic[T]):
    def generate_request(self, extractions_schema: T) -> HttpRequest:
        pass
