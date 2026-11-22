"""
    Source line ref and resolver
"""
from functools import wraps
from dataclasses import dataclass
from logging import setLoggerClass
from pathlib import Path
from inspect import signature
from typing import (
    Tuple,
    Any
)

from lark import v_args

from werbanc.core.dsl.langs import (
    BaseAst,
    AstData
)

@dataclass
class Symbol:
    names_chain: Tuple[str, ...]
    item: str
    access: str | None = None

@dataclass
class SourceLineRef:
    path: Path
    symbol: Symbol

@dataclass
class Source:
    ref: SourceLineRef
    code: str
    names: Tuple[str, ...]

class SourceResolverCache:
    def __init__(self):
        self._data: dict[Path, dict[str, Any]] = {}

    @property
    def cache(self) -> dict[Path, dict[str, Any]]:
        return self._data

    def cache_path(self, path: str | Path):
        return self.cache.setdefault(
            Path(path).resolve(),
            {"data": None, "ast": None, "symbols": {}},
        )

    def cache_data(self, path: str | Path, data: str):
        self.cache_path(path)["data"] = data

    def cache_ast(self, path: str | Path, ast: AstData):
        self.cache_path(path)["ast"] = ast

    def cache_symbol(self, path: str | Path, symbol_key, symbol_data):
        self.cache_path(path)["symbols"][symbol_key] = symbol_data

    def get_data(self, path: str | Path) -> str | None:
        return self.cache.get(Path(path).resolve(), {}).get("data")

    def get_ast(self, path: str | Path) -> AstData | None:
        return self.cache.get(Path(path).resolve(), {}).get("ast")

    def get_symbol(self, path: str | Path, symbol_key) -> Source | None:
        return self.cache.get(Path(path).resolve(), {}).get("symbols", {}).get(symbol_key)

    def clear(self, path: str | Path | None = None):
        if path is None:
            self.cache.clear()
        else:
            self.cache.pop(Path(path).resolve(), None)


def cached(method):
    method_sig = signature(method)
    cache_methods = {
        "get_data": ("cache_data", False),
        "get_ast": ("cache_ast", False),
        "get_symbol": ("cache_symbol", True),
    }

    @wraps(method)
    def wrapper(self, path: Path, cache_method, **kwargs):
        getter_name = getattr(cache_method, "__name__", None)
        if getter_name not in cache_methods:
            raise ValueError(f"Cache method {getter_name!r} not implemented")

        path = Path(path).resolve()
        bound = method_sig.bind(self, path, **kwargs)
        bound.apply_defaults()

        setter_name, uses_symbol = cache_methods[getter_name]
        getter = getattr(self._cache, getter_name)
        setter = getattr(self._cache, setter_name)
        cache_args = (path,)
        if uses_symbol:
            if "symbol_key" not in bound.arguments:
                raise ValueError("Symbol cache requires a symbol_key parameter")
            symbol_key = bound.arguments["symbol_key"]
            hash(symbol_key)  # Reject unhashable keys before executing the method.
            cache_args += (symbol_key,)

        value = getter(*cache_args)
        if value is not None:
            return value

        result = method(*bound.args, **bound.kwargs)
        setter(*cache_args, result)
        return result

    return wrapper


class SourceResolver:
    _ast: BaseAst
    _cache: SourceResolverCache

    def __init__(self, ast_parser: BaseAst):
        self._ast = ast_parser
        self._cache = SourceResolverCache()

    @cached
    def _read_source_path(self, path: Path) -> str:
        if not path.is_file():
            raise OSError(f"File {path} not a regular file")
        return path.read_text(encoding="utf-8")

    @cached
    def _ast_parse(self, path: Path) -> AstData:
        """
            Parse source
        """
        _text = self._read_source_path(
            path,
            cache_method=SourceResolverCache.get_data,
        )
        return self._ast.parse(_text)

    @cached
    def _resolve_symbol(self, path: Path, symbol_key: Tuple[str, ...]) -> Tuple[str, Tuple[str, ...]]:
        """
            Resolve source symbol
        """
        data = self._ast_parse(path=path, cache_method=SourceResolverCache.get_ast)
        return self._ast.extract(data=data, names_chain=symbol_key)

    def resolve(self, ref: SourceLineRef) -> Source:
        code, names_chain = self._resolve_symbol(
            path=ref.path,
            symbol_key=ref.symbol.names_chain,
            cache_method=SourceResolverCache.get_symbol,
        )
        return Source(
            ref=ref,
            code=code,
            names=names_chain
        )

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


