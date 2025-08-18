from pathlib import Path

from endpoint_configs.schema import EndpointConfig
from parameters.parameter import Parameter

example_config = EndpointConfig(
    name="example",
    route=Path("/example"),
    description="An example endpoint that accepts two integers a and b.",
    parameters=[
        Parameter(name='a', description="First integer", annotation=int),
        Parameter(name='b', description="Second integer", annotation=int),
    ]
)
