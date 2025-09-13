from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

from endpoint_configs.config_model import EndpointConfig
from endpoint_configs.schema import EndpointSchema
from tool_handler.tool_response import HttpRequest

S = TypeVar("S", bound=EndpointSchema)
T = TypeVar("T", bound=EndpointSchema)


class RequestGenerator(ABC, Generic[S, T]):

    def __init__(self, endpoint_config: EndpointConfig[S, T]):
        self.endpoint_config = endpoint_config

    @abstractmethod
    def generate_request(self, extractions_schema: T) -> HttpRequest:
        pass
