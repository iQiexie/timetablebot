from typing import Any


class SingletonNotInitiatedError(Exception):
    ...


class MetaSingleton(type):
    __instances: dict = {}
    __slots__ = tuple()

    def __call__(cls, *args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        if cls not in cls.__instances:
            for key in cls.__slots__:
                if not key.startswith("__") and key.lstrip("_") not in kwargs:
                    raise SingletonNotInitiatedError(
                        f"Not initiated: key: {key}, class: {cls.__name__}, slots: {cls.__slots__}"
                    )
            cls.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)

        return cls.__instances[cls]

    def clear_instance(cls) -> None:
        if cls in cls.__instances:
            cls.__instances[cls] = None
            del cls.__instances[cls]
