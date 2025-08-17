from pathlib import Path

from pydantic import BaseModel

from parameters.parameter import Parameter


class EndpointConfig(BaseModel):
    name: str
    route: Path
    description: str
    parameters: list[Parameter]
    