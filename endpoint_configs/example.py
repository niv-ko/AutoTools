from pydantic import HttpUrl

from endpoint_configs.config_model import EndpointConfig
from parameters.parameter import Parameter

example_config = EndpointConfig(
    name="example",
    route=HttpUrl("http://localhost:8000/example"),
    description="An example endpoint that accepts two integers a and b.",
    parameters=[
        Parameter[int](name='a', description="First integer", required_input=False),
        Parameter[int](name='b', description="Second integer", default=2),
    ]
)
