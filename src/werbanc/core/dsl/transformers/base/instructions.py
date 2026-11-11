"""
    Instructions block lark transformer mixin
"""
import re
from dataclasses import dataclass
from typing import List, Any

from lark import (
    v_args,
    Token,
)

from werbanc.core.dsl.transformers.base.dataclass_separate_collection import Variable

@dataclass
class TextBlock:
    mark: str
    text: str

@dataclass
class TemplateBlock:
    mark: str
    template: str

@dataclass
class PartBlock:
    name: str
    text: TextBlock |  None = None
    template:  TemplateBlock | None = None
    variables: List[Variable] | None = None

@dataclass
class Instruction:
    parts: List[PartBlock] | None = None
    text: TextBlock | None = None
    template: TemplateBlock | None = None
    variables: List[Variable] | None = None

class InstructionMixin:

    @v_args(inline=True)
    @staticmethod
    def mark_name(name: str) -> str:
        return name

    @staticmethod
    def text_block(children):
        _, mark, text = children
        mark = str(mark.value)
        text = re.sub(r"^-->end[ \t]*\Z", "", str(text.value), flags=re.MULTILINE)
        return TextBlock(mark=mark, text=text)

    @staticmethod
    def template_block(children):
        _, mark, template = children
        mark = str(mark.value)
        template = re.sub(r"^-->end[ \t]*\Z", "", str(template.value), flags=re.MULTILINE)
        return TemplateBlock(mark=mark, template=template)

    @staticmethod
    def part_block(children):
        _name = ""
        _text = None
        _template = None
        _variables = list()
        for item in children:
            if isinstance(item, Token) and item.type == "NAME":
                _name = str(item.value)
            elif isinstance(item, TextBlock):
                _text = item
            elif isinstance(item, TemplateBlock):
                _template = item
            elif isinstance(item, Variable):
                if item not in _variables:
                    _variables.append(item)
        return PartBlock(
            name=_name,
            text=_text,
            template=_template,
            variables=_variables
        )

    @staticmethod
    def instruction_entry(children):
        _parts = list()
        _text = None
        _template = None
        _variables = list()
        for item in children:
            if isinstance(item, PartBlock):
                _parts.append(PartBlock)
            elif isinstance(item, TextBlock):
                _text = item
            elif isinstance(item, TemplateBlock):
                _template = item
            elif isinstance(item, Variable):
                if item not in _variables:
                    _variables.append(item)
        return Instruction(
            parts=_parts,
            text=_text,
            template=_template,
            variables=_variables
        )

    @v_args(inline=True)
    @staticmethod
    def instructions_block(instruction):
        return instruction