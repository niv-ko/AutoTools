from typing import Type, Optional, Callable

from extraction_configs.schema import ExtractionMethod
from extractors.base import Extractor
from parameters.parameter import Parameter
from registry.base import BaseRegistry, T


class ExtractorRegistry(BaseRegistry[Extractor]):

    def get_extractor(self, extraction_method: ExtractionMethod, parameter_to_extract: Parameter) -> Extractor:
        extractor_name = extraction_method.extractor_name
        if extractor_name not in self._data:
            raise LookupError(f"Extractor {extractor_name} not found in registry: {self._data}")
        return self._data[extractor_name](parameter_to_extract, **extraction_method.kwargs)


_EXTRACTORS_REGISTRY = ExtractorRegistry()

register = _EXTRACTORS_REGISTRY.register

get_extractor = _EXTRACTORS_REGISTRY.get_extractor
