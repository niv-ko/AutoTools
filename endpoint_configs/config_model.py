import keyword
import re
from typing import Type, TypeVar, Generic

from pydantic import BaseModel, PrivateAttr, ConfigDict, Field, create_model, HttpUrl
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from endpoint_configs.schema import EndpointSchema
from parameters.parameter import Parameter, TypeLike, _NOT_GIVEN

INPUT_SCHEMA_MODEL_NAME_SUFFIX = "_input_schema"
OUTPUT_SCHEMA_MODEL_NAME_SUFFIX = "_schema"

S = TypeVar("S", bound=EndpointSchema)
T = TypeVar("T", bound=EndpointSchema)


class Unset(BaseModel):
    pass


class EndpointConfig(BaseModel, Generic[S, T]):
    model_config = ConfigDict(extra="forbid", frozen=True)
    name: str
    route: HttpUrl
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

    def get_schema_fields(self, input_schema: bool) -> dict[str, tuple[TypeLike, FieldInfo]]:
        fields = dict()

        for p in self.parameters:
            field_name = _sanitize(p.name)
            if input_schema and not p.required_input:
                default = _NOT_GIVEN
            else:
                default = p.default if p.default is not _NOT_GIVEN else ...
            fields[field_name] = (
                p.param_type(),
                Field(
                    default,
                    description=p.description,
                    alias=p.name,  # accept original name in input/output
                ),
            )
        return fields

    @property
    def endpoint_input_schema(self) -> Type[S]:
        fields = self.get_schema_fields(input_schema=True)

        model_name = f"{self.name}{INPUT_SCHEMA_MODEL_NAME_SUFFIX}"

        model = create_model(
            model_name,
            __base__=EndpointSchema,
            __config__=ConfigDict(frozen=True, extra="forbid"),
            **fields,
        )

        return model

    @property
    def endpoint_output_schema(self) -> Type[T]:
        fields = self.get_schema_fields(input_schema=False)

        model_name = f"{self.name}{OUTPUT_SCHEMA_MODEL_NAME_SUFFIX}"

        model = create_model(
            model_name,
            __base__=EndpointSchema,
            __config__=ConfigDict(frozen=True, extra="forbid"),
            **fields,
        )

        return model


def _sanitize(name: str) -> str:
    # collapse non-word chars to underscores and trim leading/trailing underscores
    s = re.sub(r'\W+', '_', name or '').strip('_')

    # fallback if everything was stripped
    if not s:
        s = 'f'

    # avoid starting with a digit
    if s[0].isdigit():
        s = f"f_{s}"

    # avoid Pydantic's protected namespace
    if s.startswith('model_'):
        s = f"f_{s}"

    # avoid Python keywords
    if keyword.iskeyword(s):
        s = f"{s}_"

    return s
