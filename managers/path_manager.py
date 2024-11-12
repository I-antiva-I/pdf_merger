import os

from pathlib import Path


class PathManager:
    base_path = Path(".")

    @classmethod
    def path_to_stylesheet(cls) -> Path:
        return Path.joinpath(cls.base_path, Path("assets/css/styles.css"))

    @classmethod
    def path_to_fonts(cls) -> Path:
        return Path.joinpath(cls.base_path, Path("assets/fonts/"))

    @classmethod
    def path_to_icons(cls) -> Path:
        return Path.joinpath(cls.base_path, Path("assets/icons/"))