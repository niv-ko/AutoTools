from types import GenericAlias, UnionType
from typing import ForwardRef, Any, TypeVar, Generic, Type, get_args

from pydantic import BaseModel
from pydantic.config import ConfigDict

TypeLike = type | GenericAlias | UnionType | ForwardRef

T = TypeVar("T")


class Parameter(BaseModel, Generic[T]):
    name: str
    description: str
    required_input: bool = False
    default: T

    def param_type(self) -> TypeLike:
        t = get_args(self.__class__)
        if not t:
            raise TypeError("Use a specialized generic, e.g. Parameter[int](...)")
        return t[0]
