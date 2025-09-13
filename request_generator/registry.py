from registry.base import BaseRegistry, T
from request_generator.base import RequestGenerator


class RequestGeneratorRegistry(BaseRegistry[RequestGenerator]):

    def get_extractor(self, generator_name: str) -> RequestGenerator:
        if generator_name not in self._data:
            raise LookupError(f"Request generator {generator_name} not found in registry: {self._data}")
        return self._data[generator_name]()


_GENERATORS_REGISTRY = RequestGeneratorRegistry()

register = _GENERATORS_REGISTRY.register

get_extractor = _GENERATORS_REGISTRY.get_extractor