import pytest
from pydantic import ValidationError

from endpoint_configs.schema import EndpointSchema
from parameters.parameter import Parameter
from parameter_extraction.parameter_extraction import ParameterExtraction


class SimpleSchema(EndpointSchema):
    foo: str
    bar: int | None = None


class StrictSchema(EndpointSchema):
    a: int
    b: float


def pe(param_name: str, type_, value):
    P = Parameter[type_]
    return ParameterExtraction[type_](parameter=P(name=param_name, description="d"), result=value)


def test_from_extractions_happy_path_populates_and_validates():
    exts = [
        pe("foo", str, "hello"),
        pe("bar", int, 5),
    ]
    m = SimpleSchema.from_extractions(exts)
    assert m.foo == "hello"
    assert m.bar == 5


def test_missing_optional_field_uses_default_none():
    exts = [pe("foo", str, "hi")]
    m = SimpleSchema.from_extractions(exts)
    assert m.foo == "hi"
    assert m.bar is None


def test_coercion_applies_via_type_adapter():
    class S(EndpointSchema):
        n: int
        f: float

    exts = [
        pe("n", int, "7"),
        pe("f", float, 3),
    ]
    m = S.from_extractions(exts)
    assert m.n == 7
    assert m.f == 3.0


def test_invalid_required_raises_validation_error():
    # Create an extraction typed as str for field 'a' which schema expects to be int
    P_str = Parameter[str]
    bad = ParameterExtraction[str](parameter=P_str(name="a", description="d"), result="bad")
    good = pe("b", float, 1.2)
    with pytest.raises(ValidationError):
        StrictSchema.from_extractions([bad, good])


def test_unknown_parameter_names_are_ignored():
    exts = [pe("foo", str, "ok"), pe("unknown", int, 1)]
    m = SimpleSchema.from_extractions(exts)
    assert m.foo == "ok"
    assert m.bar is None


def test_all_missing_required_raises():
    with pytest.raises(ValidationError):
        SimpleSchema.from_extractions([])


def test_none_for_optional_is_accepted():
    exts = [pe("foo", str, "x"), pe("bar", int | None, None)]
    m = SimpleSchema.from_extractions(exts)
    assert m.foo == "x"
    assert m.bar is None


def test_none_for_required_raises():
    exts = [pe("foo", str, None)]
    with pytest.raises(ValidationError):
        SimpleSchema.from_extractions(exts)


def test_duplicate_extractions_last_wins():
    exts = [pe("foo", str, "first"), pe("foo", str, "second")]
    m = SimpleSchema.from_extractions(exts)
    assert m.foo == "second"
