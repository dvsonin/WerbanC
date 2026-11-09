"""
    Firs transformer
"""
from enum import (
    Enum,
    member
)

from dataclasses import dataclass
from typing import Tuple, List

from lark import (
    Transformer,
    v_args
)

from werbanc.core.dsl.transformers.base import source_line as src_line
from werbanc.core.dsl.transformers.base import batch_iterate
from werbanc.core.dsl.langs import BaseAstMixin
from werbanc.core.dsl.langs.python import ASTPython

class AstNotImplemented(Exception):
    pass

class UndefinedError(Exception):
    pass


class AstSelector(Enum):
    PYTHON = member(ASTPython)

@dataclass
class GlobalSettings:
    lang_ast: type[BaseAstMixin]
    batch_iterate: List[dict[str, tuple]] | None = None
    context: Tuple[src_line.SourceLineRef] | None = None

class BaseTransformer(
    Transformer,
    src_line.SourceLineTransformerMixin,
    batch_iterate.BatchIterateMixin
):

    @v_args(inline=True)
    @staticmethod
    def lang_definition(lang: str) -> type[BaseAstMixin]:
        return AstSelector[lang.upper()].value

    @staticmethod
    def context_block(children) -> Tuple[src_line.SourceLineRef]:
        return tuple(children)

    @v_args(inline=True)
    @staticmethod
    def global_block(
            lang: type[BaseAstMixin],
            iterate_over: List[dict[str, tuple]] | None = None,
            context: Tuple[src_line.SourceLineRef] | None =  None
    ) -> GlobalSettings:
        return GlobalSettings(
            lang_ast=lang,
            batch_iterate=iterate_over,
            context=context
        )