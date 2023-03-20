"""
URL operator module.
"""
import abc
from functools import lru_cache
import importlib
import importlib.util
from pathlib import Path
import re
from typing import Tuple, Type, Union

from core.util import snake_to_camel


BASE_DIR = 'operators'
BASE_PATH = (Path(__file__).parent.absolute() / f"../{BASE_DIR}").resolve()


class OperatorInterface(metaclass=abc.ABCMeta):
    """Interface for operators."""

    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    priority = 1

    @classmethod
    def __subclasshook__(cls, __subclass) -> bool:
        return (
            hasattr(__subclass, "url_patterns")
            and callable(__subclass.url_patterns)  # type: ignore
            and hasattr(__subclass, "main")
            and callable(__subclass.main)  # type: ignore
            or NotImplemented
        )

    @classmethod
    @abc.abstractmethod
    def url_patterns(cls) -> list:
        """URL patterns of the operator."""

    @abc.abstractmethod
    async def main(self, url: str) -> dict:
        """Main function of the operator."""


def get_operator(operator_path: Path) -> Union[Type[OperatorInterface], None]:
    """Get operator class from file path."""
    try:
        name = operator_path.stem
        module = importlib.import_module(f"{BASE_DIR}.{name}")
        # get class from module
        class_name = snake_to_camel(name)
        operator = module.__dict__[class_name]
        if issubclass(operator, OperatorInterface):
            return operator
        return None
    except (ImportError, AttributeError, SyntaxError) as err:
        raise err


@lru_cache(maxsize=1)
def list_operators():
    """List all operators."""
    res: list[Tuple[Union[str, re.Pattern], int, Type[OperatorInterface]]] = []

    for operator_file in BASE_PATH.glob("[!_]*.py"):
        operator = get_operator(operator_file)
        if operator is not None:
            # flat patterns
            for s in operator.url_patterns():
                pattern = re.compile(s) if s.startswith('https?') else s
                res.append((pattern, operator.priority, operator))

    # sort by priority
    res.sort(key=lambda x: x[1], reverse=True)

    return res


@lru_cache(maxsize=128)
def match_operator(url: str) -> Union[Type[OperatorInterface], None]:
    """Match operator from URL."""
    for (pattern, _, operator) in list_operators():
        if (pattern == url
            if isinstance(pattern, str)
                else pattern.match(url)):
            return operator
    return None
