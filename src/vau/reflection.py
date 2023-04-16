"""
A helper module to reflect on runtime objects, their methods and attributes. Allows you to build a proxy object that
behaves like the original object, but with some modifications.
"""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable, Iterable, TypeVar, cast

from wrapt import ObjectProxy

T = TypeVar("T")


class Method:
    def __init__(self, refl: Reflection, name: str) -> None:
        self.name = name
        self._refl = refl
        self._signature: inspect.Signature | None = None
        self.kwargs: dict[str, Any] = {}

    @property
    def original(self) -> Callable[..., Any]:
        return getattr(self._refl._obj, self.name)

    @property
    def signature(self) -> inspect.Signature:
        if self._signature is None:
            self._signature = inspect.signature(self.original)
        return self._signature

    def build(self) -> Callable[..., Any]:
        original = self.original
        if not self.kwargs:
            return original

        @functools.wraps(original)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return original(*args, **{**self.kwargs, **kwargs})

        return wrapper


class Reflection:
    def __init__(self, obj: Any) -> None:
        self._obj = obj
        self._methods: dict[str, Method] = {}

    def methods(self) -> Iterable[Method]:
        # NOTE(@NiklasRosenstein): inspect.signature() won't work with e.g. __subclasshook__ and __init_subclass__.
        return (
            self.method(name)
            for name in dir(self._obj)
            if callable(getattr(self._obj, name))
            if not name.startswith("__")
        )

    def method(self, name: str) -> Method:
        if name not in self._methods:
            self._methods[name] = Method(self, name)
        return self._methods[name]

    def into(self, cls: type[T]) -> T:
        """Creates an #ObjectProxy that behaves like the original object, but with some modifications."""

        # NOTE(@NiklasRosenstein): Dirty hack because we can't use object.__setattr__ on an #ObjectProxy
        #       without also setting the WRAPT_DISABLE_EXTENSIONS environment variable. See this issue:
        #       https://github.com/GrahamDumpleton/wrapt/issues/235
        attrs = {}
        for method in self._methods.values():
            attrs[method.name] = staticmethod(method.build())

        proxy_cls = type("Proxy", (ObjectProxy,), attrs)
        proxy = proxy_cls(self._obj)
        return cast(T, proxy)
