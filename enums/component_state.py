from enum import Enum


class ComponentState(Enum):
    DEFAULT = 0
    HOVERED = 1
    PRESSED = 2
    CHECKED = 3
    UNCHECKED = 4
    CHECKED_DEFAULT = 11
    CHECKED_HOVERED = 11