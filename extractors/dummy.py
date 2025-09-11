from typing import Any

from extractors.base import Extractor
from parameter_extraction.parameter_extraction import ParameterExtraction


class DummyExtractor(Extractor):
    def extract(self, **kwargs) -> Any:
        print(f"Dummy extractor called with parameter {self.parameter_to_extract.name}")
        return None
