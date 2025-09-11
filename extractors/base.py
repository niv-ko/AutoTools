from typing import Any

from parameter_extraction.parameter_extraction import ParameterExtraction
from parameters.parameter import Parameter


class Extractor:
    def __init__(self, parameter_to_extract: Parameter, **kwargs):
        self.parameter_to_extract = parameter_to_extract
        self.kwargs = kwargs

    def extract(self, required_extractions: list[ParameterExtraction], **kwargs) -> Any:
        raise NotImplementedError("Extractor.extract must be implemented in subclasses.")

    def __call__(self, *args, **kwargs):
        return self.extract(*args, **kwargs)
