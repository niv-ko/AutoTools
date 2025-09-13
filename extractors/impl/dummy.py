from typing import Any

from extractors.base import Extractor
from extractors.registry import register
from parameter_extraction.parameter_extraction import ParameterExtraction

@register(name="dummy")
class DummyExtractor(Extractor):
    async def extract(self, required_extractions: list[ParameterExtraction], **kwargs) -> Any:
        print(f"Dummy extractor called with parameter {self.parameter_to_extract.name}")
        return None
