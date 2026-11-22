"""
    Python AST parser
"""
import ast
from typing import Tuple

from werbanc.core.dsl.langs import (
    BaseAst,
    AstData
)

class ASTPython(BaseAst):
    _supported_nodes = (
        ast.ClassDef,
        ast.FunctionDef,
        ast.AsyncFunctionDef
    )

    def parse(self, text: str) -> AstData:
        """
            Parse Python sources
        """
        return AstData(
            text=text,
            tree=ast.parse(text),
        )

    def extract(self, data: AstData, names_chain: tuple[str, ...]) -> Tuple[str, Tuple[str]]:
        """
            Extract source symbol from ast tree
        """
        if not names_chain:
            raise ValueError(f"Empty names chain")

        _scope = data.tree
        for name in names_chain:
            _matches = [
                node
                for node in getattr(_scope, "body", [])
                if isinstance(node, self._supported_nodes) and node.name == name
            ]

            if not _matches:
                raise LookupError(
                    f"Symbol {'.'.join(names_chain)!r} not found." 
                    f"Missed {name!r}"
                )

            if len(_matches) > 1:
                raise LookupError(
                    f"Multiple symbol definition found {name!r}: {len(_matches)}"
                )
            _scope = _matches[0]

        code = ast.get_source_segment(data.text, _scope)

        if code is None:
            raise ValueError(
                f"Code extraction fail {'.'.join(names_chain)!r}"
            )

        return code, names_chain



