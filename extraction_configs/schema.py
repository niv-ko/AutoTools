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
    parameter_extraction_methods: list[ParameterExtractionMethod]
    parameters_requirements: list[ParameterRequirement] = Field(default_factory=list)

    _method_by_name: dict[str, ExtractionMethod] = Field(default_factory=dict)
    _requirements_by_name: dict[str, list[str]] = Field(default_factory=dict)

    def model_post_init(self, __context):
        # Build private indices for quick access
        self._method_by_name.update(
            {pem.parameter_name: pem.extraction_method for pem in self.parameter_extraction_methods})
        self._requirements_by_name.update({param_reqs.parameter_name: param_reqs.required_parameters_names
                                           for param_reqs in self.parameters_requirements})

    def get_extraction_method(self, parameter_name: str) -> ExtractionMethod:
        try:
            return self._method_by_name[parameter_name]
        except KeyError:
            raise KeyError(f"Extraction method for parameter '{parameter_name}' not found.") from None

    def get_required_parameters(self, parameter_name: str) -> list[str]:
        try:
            return self._requirements_by_name[parameter_name]
        except KeyError:
            raise KeyError(f"Required parameters for '{parameter_name}' not found.") from None
