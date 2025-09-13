from typing import Generic, TypeVar

from pydantic import HttpUrl

from endpoint_configs.schema import EndpointSchema
from request_generator.base import RequestGenerator
from tool_handler.tool_response import HttpRequest

S = TypeVar("S", bound=EndpointSchema)
T = TypeVar("T", bound=EndpointSchema)


class DummyRequestGenerator(RequestGenerator, Generic[S, T]):
    def generate_request(self, extractions_schema: T) -> HttpRequest:
        return HttpRequest(
            url=self.endpoint_config.route,
            method="GET",
            headers={},
            params={},
            body=extractions_schema.model_dump_json()
        )
