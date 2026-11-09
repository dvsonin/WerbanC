"""
    Base for ast works
"""

from pathlib import Path
from typing import Tuple


class BaseAstMixin:
    _sources_paths: list[str]
    _sources_data: dict[str, Tuple[str, Path]]

    @property
    def sources_paths(self) -> list[str]:
        return self._sources_paths

    def sources_paths_append(self, path: str) -> None:
        """
            Append path to sources
        """
        if path not in self._sources_paths:
            self._sources_paths.append(path)

    def read_source(self, path: str, reload: bool) -> str:
        """
            Read source from path
        """
        data = self._sources_data.get(path)
        if data is not None:
            if reload:
                _, _path_obj = self._sources_data[path]
                data = _path_obj.read_text(encoding="utf-8")
                self._sources_data[path] = (data, _path_obj)
                return data

        _path_obj = Path(path)
        if not _path_obj.is_file():
            raise OSError(f"{path} is not a regular file")
        data = _path_obj.read_text(encoding="utf-8")
        self._sources_data[path] = (data, _path_obj)
        return data


