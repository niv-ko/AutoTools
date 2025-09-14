import asyncio
from abc import ABC, abstractmethod
from typing import Any

from exceptions.extraction_error import ExtractionError
from parameter_extraction.parameter_extraction import ParameterExtraction
from parameters.parameter import Parameter


class Extractor(ABC):
    def __init__(self, parameter_to_extract: Parameter, **kwargs):
        self.parameter_to_extract = parameter_to_extract
        self.kwargs = kwargs

    @abstractmethod
    async def extract(self, query: str, required_extractions: list[ParameterExtraction], **kwargs) -> Any:
        pass

    async def __call__(self, query: str, required_extractions: list[ParameterExtraction], **kwargs):
        try:
            return await self.extract(query, required_extractions, **kwargs)
        except asyncio.CancelledError:
            raise
        except (SystemExit, KeyboardInterrupt, GeneratorExit):
            raise
        except Exception as e:
            raise ExtractionError(extractor_name=self.__class__.__name__,
                                  parameter_name=self.parameter_to_extract.name) from e
