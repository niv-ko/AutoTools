from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

from tool_handler.tool_response import HttpRequest

TModel = TypeVar("TModel", bound=BaseModel)


@abstractmethod
class RequestGenerator(ABC, Generic[TModel]):
    def generate_request(self, extractions_schema: TModel) -> HttpRequest:
        pass
