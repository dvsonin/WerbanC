"""
    Base for ast works
"""
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class AstData:
    text: str
    encode: bytes | None = None

class BaseAst:

     @abstractmethod
     def parse(self, text: str) -> AstData:
        raise NotImplemented

