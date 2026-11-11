"""
    Firs transformer
"""
from enum import (
    Enum,
    member
)

from dataclasses import dataclass
from logging import setLogRecordFactory
from typing import Tuple, List, Dict, Any

from lark import (
    Transformer,
    v_args
)

from werbanc.core.dsl.transformers.base import source_line as src_line
from werbanc.core.dsl.transformers.base import batch_iterate
from werbanc.core.dsl.transformers.base import instructions
from werbanc.core.dsl.transformers.base.dataclass_separate_collection import Variable
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

@dataclass
class Task:
    global_settings: GlobalSettings
    instruction: instructions.Instruction
    variables: List[Variable]

@dataclass
class WerbancSript:
    tasks: Dict[str, Task]

class BaseTransformer(
    Transformer,
    src_line.SourceLineTransformerMixin,
    batch_iterate.BatchIterateMixin,
    instructions.InstructionMixin
):
    _vars: List[Variable]

    def __init__(self,  visit_tokens: bool=True):
        super().__init__(visit_tokens)
        self._vars = list()


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

    @v_args(inline=True)
    def assign_var(self, name, value) -> Variable:
        var = Variable(name=name.value, value=value)
        if var not in self._vars:
            self._vars.append(var)
        return var

    @v_args(inline=True)
    def task_block(self, global_settings, instruction):
        return Task(
            global_settings=global_settings,
            instruction=instruction,
            variables=self._vars
        )

    @staticmethod
    def task(children):
        if len(children) == 1:
            return "task", children[0]
        name, body = children
        return str(name), body

    @staticmethod
    def start(children):
        tasks = {}

        for name, body in children:
            if name in tasks:
                raise ValueError(f"Task {name} duplicate")
            tasks[name] = body
        return WerbancSript(tasks=tasks)