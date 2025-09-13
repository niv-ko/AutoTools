from types import GenericAlias, UnionType, EllipsisType
from typing import ForwardRef, Any, TypeVar, Generic, Type, get_args

from pydantic import BaseModel
from pydantic.config import ConfigDict

TypeLike = type | GenericAlias | UnionType | ForwardRef

T = TypeVar("T")
_NOT_GIVEN = object()

class Parameter(BaseModel, Generic[T]):
    name: str
    description: str
    required_input: bool = False
    # has_default: bool = False
    default: T = _NOT_GIVEN

    @classmethod
    def param_type(cls) -> Type[T]:
        md = getattr(cls, "__pydantic_generic_metadata__", None)
        if md and md.get("args"):
            return md["args"][0]
        raise TypeError(f"{cls.__name__} must be specialized, e.g. {cls.__name__}[int]")
