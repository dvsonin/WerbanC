"""
    Lark WerbanC DSL parser
"""
from importlib.resources import files
from lark import (
    Lark,
    Tree,
)

from werbanc.core.dsl.transformers.base import BaseTransformer


class DSLParser:

    def __init__(self) -> None:
        grammar = (
            files("werbanc.core").joinpath("werbanc.lark").read_text(encoding="utf-8")
        )
        self._parser = Lark(
            grammar,
            parser="lalr",
            lexer="contextual",
            propagate_positions=True,
            transformer=BaseTransformer()
        )

    def parse(self, source: str) -> Tree:
        return self._parser.parse(source)