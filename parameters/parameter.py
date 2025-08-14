from typing import Type

from pydantic import BaseModel, Field


class Parameter(BaseModel):
    name: str
    description: str
    type: BaseModel
