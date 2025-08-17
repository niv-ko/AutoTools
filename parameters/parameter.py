from types import GenericAlias, UnionType
from typing import ForwardRef

from pydantic import BaseModel
from pydantic.config import ConfigDict

TypeLike = type | GenericAlias | UnionType | ForwardRef


class Parameter(BaseModel):

    name: str
    description: str
    annotation: TypeLike
