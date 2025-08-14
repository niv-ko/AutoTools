from pydantic import BaseModel, Field, conlist


class ExtractionMethod(BaseModel):
    extractor_name: str
    kwargs: dict[str, str] = Field(default_factory=dict)


class ParameterExtractionMethod(BaseModel):
    parameter_name: str
    extraction_method: ExtractionMethod


class ParameterRequirement(BaseModel):
    parameter_name: str
    required_parameters_names: conlist(str, min_length=1)


class ExtractionConfig(BaseModel):
    parameter_extraction_methods: list[ExtractionMethod]
    parameters_requirements: list[ParameterRequirement] = Field(default_factory=list)
