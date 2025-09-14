import pytest
from pydantic import ValidationError

from endpoint_configs.config_model import (
    EndpointConfig,
    INPUT_SCHEMA_MODEL_NAME_SUFFIX,
    OUTPUT_SCHEMA_MODEL_NAME_SUFFIX,
    _sanitize,
)
from endpoint_configs.schema import EndpointSchema
from parameters.parameter import Parameter


def make_params():
    StrParam = Parameter[str]
    IntParam = Parameter[int]

    p1 = StrParam(name="foo", description="req str", required_input=True)
    p2 = StrParam(name="bar-baz", description="optional in", required_input=False)
    p3 = IntParam(name="9lives", description="has default", required_input=True, default=9)
    return p1, p2, p3


essential_route = "https://example.com/api/echo"


def make_config(params=None, name="echo"):
    if params is None:
        params = list(make_params())
    return EndpointConfig(
        name=name,
        route=essential_route,
        description="Test endpoint",
        parameters=params,
    )


def test_duplicate_parameter_names_raise():
    P = Parameter[str]
    p1 = P(name="dup", description="one", required_input=True)
    p2 = P(name="dup", description="two", required_input=False)
    with pytest.raises(ValueError, match="Duplicate parameter names\."):
        make_config([p1, p2])


def test_get_param_by_name_and_error():
    p1, p2, p3 = make_params()
    cfg = make_config([p1, p2, p3])

    assert cfg.get_param_by_name("foo") is p1
    assert cfg.get_params_by_names(["bar-baz", "foo"]) == [p2, p1]

    with pytest.raises(KeyError) as ei:
        cfg.get_param_by_name("missing")
    assert "Parameter 'missing' not found in endpoint 'echo'." == ei.value.args[0]


def test_input_schema_generation_and_alias_handling():
    p1, p2, p3 = make_params()
    cfg = make_config([p1, p2, p3], name="hello")

    InputSchema = cfg.endpoint_input_schema

    # class basics
    assert issubclass(InputSchema, EndpointSchema)
    assert InputSchema.__name__ == f"hello{INPUT_SCHEMA_MODEL_NAME_SUFFIX}"

    # only required_input fields must be necessary
    data = {"foo": "hi", "9lives": 42}  # use original names via alias
    m = InputSchema(**data)

    # sanitized fields are present and mapped correctly
    assert m.foo == "hi"
    assert getattr(m, "f_9lives") == 42

    # optional input (bar-baz) should not be required and absent fields should not cause validation errors
    assert "bar_baz" not in m.model_fields_set

    # extra should be forbidden
    with pytest.raises(ValidationError):
        InputSchema(**{**data, "extra": 1})

    # frozen should prevent mutation
    with pytest.raises(ValidationError):
        setattr(m, "foo", "nope")


def test_output_schema_generation_and_requirements():
    p1, p2, p3 = make_params()
    cfg = make_config([p1, p2, p3], name="goodbye")

    OutputSchema = cfg.endpoint_output_schema

    assert issubclass(OutputSchema, EndpointSchema)
    assert OutputSchema.__name__ == f"goodbye{OUTPUT_SCHEMA_MODEL_NAME_SUFFIX}"

    # For output schema: fields with no explicit default are required.
    # p1 (foo) required, p2 (bar-baz) required, p3 (9lives) has default=9 and is optional
    data = {"foo": "yo", "bar-baz": "opt"}
    m = OutputSchema(**data)

    assert m.foo == "yo"
    assert getattr(m, "bar_baz") == "opt"
    # default applied for p3
    assert getattr(m, "f_9lives") == 9

    # missing required should fail
    with pytest.raises(ValidationError):
        OutputSchema(**{"foo": "yo"})


def test_sanitize_edge_cases():
    # empty name becomes prefixed with 'f_'
    assert _sanitize("") == "f"
    # invalid characters replaced
    assert _sanitize("a b-c") == "a_b_c"
    # leading digits get prefixed with 'f_'
    assert _sanitize("123x") == "f_123x"


def test_alias_metadata_in_fields():
    p = Parameter[str](name="sp ace", description="x", required_input=True)
    cfg = make_config([p])

    InputSchema = cfg.endpoint_input_schema
    # Field is sanitized and alias preserved
    assert "sp_ace" in InputSchema.model_fields
    assert InputSchema.model_fields["sp_ace"].alias == "sp ace"

    # Accept alias on input
    m = InputSchema(**{"sp ace": "ok"})
    assert m.sp_ace == "ok"
