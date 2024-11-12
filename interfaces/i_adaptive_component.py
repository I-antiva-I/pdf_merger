from abc import abstractmethod, ABCMeta

from PyQt5.QtWidgets import QWidget

from enums.display_mode import DisplayMode


class IAdaptiveComponentMeta(ABCMeta, type(QWidget)):
    pass


class IAdaptiveComponent(metaclass=IAdaptiveComponentMeta):

    @property
    @abstractmethod
    def display_mode(self) -> DisplayMode:
        pass

    @display_mode.setter
    @abstractmethod
    def display_mode(self, value: DisplayMode) -> None:
        pass

    @abstractmethod
    def rearrange_content(self) -> None:
        pass
