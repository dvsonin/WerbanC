"""
    Source line ref and resolver
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from lark import v_args

@dataclass
class Symbol:
    names_chain: str
    item: str
    access: str | None = None

@dataclass
class SourceLineRef:
    path: Path
    symbol: Symbol

class SourceLineTransformerMixin:
    """
        Transformer mixin for source line
    """

    @staticmethod
    def symbol_name(children):
        return tuple(str(name) for name in children)

    @v_args(inline=True)
    @staticmethod
    def symbol_item(item):
        return str(item)

    @v_args(inline=True)
    @staticmethod
    def source_path(path) -> Path:
        return Path(path)

    @v_args(inline=True)
    @staticmethod
    def symbol_attr(attr):
        return str(attr)

    @v_args(inline=True)
    @staticmethod
    def symbol_access(access):
        return str(access)

    @v_args(inline=True)
    @staticmethod
    def src_symbol(names_chain, item, access = None) -> Symbol:
        return Symbol(
            names_chain=names_chain,
            item=item,
            access=access
        )

    @v_args(inline=True)
    @staticmethod
    def source_line(path: Path, symbol: Symbol) -> SourceLineRef:
        return SourceLineRef(
            path=path,
            symbol=symbol
        )

    @staticmethod
    def source_lines(children) -> Tuple[SourceLineRef]:
        return tuple(children)


