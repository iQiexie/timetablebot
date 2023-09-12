from typing import Any, Callable

from app.backend.core.exceptions.runtime import EmptyArgumentsError


def expect_arguments(func: Callable) -> Callable:
    async def wrapper(*args, **kwargs) -> Any:
        arguments: tuple = func.__code__.co_varnames[: func.__code__.co_argcount]  # noqa

        if not kwargs and len(args) < 2 and arguments != ("self",):  # noqa
            raise EmptyArgumentsError(arguments)

        for _key, value in kwargs.items():
            if value is not None:
                return await func(*args, **kwargs)

        raise EmptyArgumentsError(arguments=arguments[1:] if "self" in arguments else arguments)

    return wrapper


def expect_specific_arguments(arguments: tuple[str, ...]) -> Callable:
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> Any:
            arguments_in_args = any(i in arguments for i in args)
            arguments_in_kwargs = any(key in arguments and value is not None for key, value in kwargs.items())

            if (not arguments_in_args) and (not arguments_in_kwargs):
                raise EmptyArgumentsError(arguments=arguments)

            return await func(*args, **kwargs)

        return wrapper

    return decorator
