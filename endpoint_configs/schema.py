from pathlib import Path

from pydantic import BaseModel, PrivateAttr, ConfigDict

from parameters.parameter import Parameter


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
