from typing import Type, Optional, Callable

from extraction_configs.schema import ExtractionMethod
from extractors.base import Extractor
from parameters.parameter import Parameter


class ExtractorRegistry:
    def __init__(self):
        self._data: dict[str, Type[Extractor]] = dict()

    def add_extractor(self, extractor_type: Type[Extractor], name: Optional[str]):
        key = getattr(extractor_type, 'name', name)
        if key in self._data:
            raise NameError(f"Duplicate extractor name '{key}' in registry!")
        if key is None:
            raise NameError("Registered extractor must have a name")
        self._data[key] = extractor_type

    def get_extractor(self, extraction_method: ExtractionMethod, parameter_to_extract: Parameter) -> Extractor:
        extractor_name = extraction_method.extractor_name
        if extractor_name not in self._data:
            raise LookupError(f"Extractor {extractor_name} not found in registry: {self._data}")
        return self._data[extractor_name](parameter_to_extract, **extraction_method.kwargs)


_METRICS_REGISTRY = ExtractorRegistry()


def register(name: Optional[str] = None) -> Callable[[Type[Extractor]], Type[Extractor]]:
    def decorator(extractor_type: Type[Extractor]) -> Type[Extractor]:
        _METRICS_REGISTRY.add_extractor(extractor_type, name)
        return extractor_type

    return decorator


def get_extractor(extraction_method: ExtractionMethod, parameter_to_extract: Parameter) -> Extractor:
    return _METRICS_REGISTRY.get_extractor(extraction_method, parameter_to_extract)
