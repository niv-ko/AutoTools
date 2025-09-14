from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from endpoint_configs.schema import EndpointSchema
from tool_handler.tool_response import Explanations

T = TypeVar('T', bound=EndpointSchema)


class ResponseExplainer(ABC, Generic[T]):
    @abstractmethod
    async def explain_extractions(self, extractions_schema: T) -> Explanations:
        pass
