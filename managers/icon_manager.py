from pathlib import Path
from typing import Dict

from enums.svg_icon import SVGIcon
from managers.path_manager import PathManager


class IconManager:
    icon_paths: Dict[SVGIcon, Path] = {
        SVGIcon.CHECKBOX_INDICATOR:     PathManager.path_to_icons().joinpath("checkbox_indicator.svg"),
        SVGIcon.CIRCLE_REMOVE:          PathManager.path_to_icons().joinpath("circle-xmark-regular.svg"),
        SVGIcon.FILE_PLUS:              PathManager.path_to_icons().joinpath("file-earmark-plus.svg"),
        SVGIcon.FILE_BREAK:             PathManager.path_to_icons().joinpath("file-earmark-break.svg"),
        SVGIcon.GRID:                   PathManager.path_to_icons().joinpath("grid-3x3-gap-fill.svg"),
        SVGIcon.LIST:                   PathManager.path_to_icons().joinpath("list-solid.svg"),
        SVGIcon.LIGHTNING:              PathManager.path_to_icons().joinpath("lightning-charge.svg"),
    }

    @classmethod
    def get_path(cls, svg_icon: SVGIcon) -> str:
        path = cls.icon_paths.get(svg_icon, None)
        if path is not None:
            return str(path)
        else:
            raise ValueError(f"No path for the given SVGIcon: {svg_icon}")