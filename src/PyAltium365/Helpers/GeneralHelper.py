from functools import wraps
from typing import Type, TypeVar, Callable, Any, cast, no_type_check

F = TypeVar('F', bound=Callable[..., Any])


class ReturnOnException:
    def __init__(self, ret: Any = None, exception: Type[Exception] = Exception) -> None:
        self._exception = exception
        self._return = ret

    def __call__(self, func: F) -> F:
        @wraps(func)
        @no_type_check
        def func_wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except self._exception:
                return self._return
        return cast(F, func_wrapper)
