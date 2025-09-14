from __future__ import annotations

from typing import TypeVar, Generic

from pydantic import BaseModel

from parameters.parameter import Parameter

T = TypeVar("T")

class ParameterExtraction(BaseModel, Generic[T]):
    parameter: Parameter[T]
    result: T | None

    # @model_validator(mode='after')
    # def validate_result_matches_parameter(self) -> ParameterExtraction:
    #     expected = self.parameter.annotation
    #     try:
    #         self.result = TypeAdapter(expected).validate_python(self.result)
    #     except ValidationError as e:
    #         raise ValueError(f'result does not match expected type {expected!r}: {e}') from e
    #
    #     return self
