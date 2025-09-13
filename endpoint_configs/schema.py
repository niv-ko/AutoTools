from __future__ import annotations

from dataclasses import fields

from pydantic import BaseModel, TypeAdapter, ValidationError

from parameter_extraction.parameter_extraction import ParameterExtraction


class EndpointSchema(BaseModel):

    @classmethod
    def from_extractions(cls, extractions: list[ParameterExtraction]) -> EndpointSchema:
        schema_data = {}
        fields_values = {pe.parameter.name: pe.result for pe in extractions}
        for field_name, field_info in cls.model_fields.items():
            if field_name not in fields_values:
                continue
            adapter = TypeAdapter(field_info.annotation)
            try:
                schema_data[field_name] = adapter.validate_python(fields_values[field_name])
            except ValidationError as e:
                print("Validation error:", e)
        return cls.model_validate(schema_data)


