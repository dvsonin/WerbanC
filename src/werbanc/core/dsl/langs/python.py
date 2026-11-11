"""
    Python AST parser
"""
import ast
from werbanc.core.dsl.langs import (
    BaseAst,
    AstData
)

class ASTPython(BaseAst):

    def parse(self, text: str) -> AstData:
        """
            Parse python sources
        """
        return AstData(
            text=ast.parse(text, mode="exec")
        )