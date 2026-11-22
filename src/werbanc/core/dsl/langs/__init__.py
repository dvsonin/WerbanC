"""
    Base for ast works
"""
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import (
    Any,
    Tuple
)

@dataclass
class AstData:
    text: str
    tree: Any
    encoded: bytes | None = None


class BaseAst(ABC):

    @abstractmethod
    def parse(self, text: str) -> AstData:
        raise NotImplementedError


    @abstractmethod
    def extract(self, data: AstData, names_chain: tuple[str, ...]) -> Tuple[str, Tuple[str]]:
        raise NotImplementedError
