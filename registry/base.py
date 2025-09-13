from abc import ABC
from typing import TypeVar, Generic, Type, Optional, Callable, get_args

T = TypeVar("T")


class BaseRegistry(ABC, Generic[T]):
    def __init__(self):
        self._data: dict[str, Type[T]] = dict()
        self.registry_type_name = self.get_registry_type_name()

    def add_subclass(self, subclass: Type[T], name: Optional[str]):
        key = getattr(subclass, 'name', name)
        if key in self._data:
            raise NameError(f"Duplicate {self.registry_type_name} name '{key}' in registry!")
        if key is None:
            raise NameError(f"Registered {self.registry_type_name} must have a name")
        self._data[key] = subclass

    @classmethod
    def get_registry_type_name(cls) -> str:
        (t,) = get_args(cls.__orig_bases__[0])  # type: ignore[attr-defined]
        return t.__name__

    def register(self, name: Optional[str] = None) -> Callable[[Type[T]], Type[T]]:
        def decorator(subclass: Type[T]) -> Type[T]:
            self.add_subclass(subclass, name)
            return subclass

        return decorator
