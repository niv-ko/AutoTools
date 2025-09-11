import re
from pathlib import Path
from typing import Type

from pydantic import BaseModel, PrivateAttr, ConfigDict, Field, create_model

from parameters.parameter import Parameter

SCHEMA_MODEL_NAME_SUFFIX = "_schema"


class EndpointConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    route: Path
    description: str
    parameters: list[Parameter]

    _by_name: dict[str, Parameter] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context):
        # tiny uniqueness check
        if len({p.name for p in self.parameters}) != len(self.parameters):
            raise ValueError("Duplicate parameter names.")
        # private index
        self._by_name.update({p.name: p for p in self.parameters})

    def get_param_by_name(self, name: str) -> Parameter:
        try:
            return self._by_name[name]
        except KeyError:
            raise KeyError(f"Parameter '{name}' not found in endpoint '{self.name}'.") from None

    def get_params_by_names(self, names: list[str]) -> list[Parameter]:
        return [self.get_param_by_name(name) for name in names]

    @property
    def endpoint_schema(self) -> Type[BaseModel]:
        fields = dict()

        for p in self.parameters:
            field_name = _sanitize(p.name)
            fields[field_name] = (
                p.annotation,
                Field(
                    default=None,
                    description=p.description,
                    alias=p.name,  # accept original name in input/output
                ),
            )

        model_name = f"{self.name}{SCHEMA_MODEL_NAME_SUFFIX}"

        model = create_model(
            model_name,
            __config__=ConfigDict(frozen=True, extra="forbid"),
            __module__=__name__,
            **fields,
        )

        return model


def _sanitize(name: str) -> str:
    # valid Python identifier
    name2 = re.sub(r'\W|^(?=\d)', '_', name)
    if name2 == "":
        name2 = "_"
    return name2
