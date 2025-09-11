from __future__ import annotations
from pydantic import BaseModel, TypeAdapter, ValidationError, model_validator
from typing import Self, Any

from parameters.parameter import Parameter, TypeLike


class ParameterExtraction(BaseModel):
    parameter: Parameter
    result: Any

    @model_validator(mode='after')
    def validate_result_matches_parameter(self) -> ParameterExtraction:
        expected = self.parameter.annotation
        try:
            self.result = TypeAdapter(expected).validate_python(self.result)
        except ValidationError as e:
            raise ValueError(f'result does not match expected type {expected!r}: {e}') from e

        return self
