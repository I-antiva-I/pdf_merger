from abc import abstractmethod, ABCMeta

from PyQt5.QtWidgets import QWidget


class IMinimizableComponentMeta(ABCMeta, type(QWidget)):
    pass


class IMinimizableComponent(metaclass=IMinimizableComponentMeta):

    @property
    @abstractmethod
    def is_minimized(self) -> bool:
        pass

    @is_minimized.setter
    @abstractmethod
    def is_minimized(self, value: bool):
        pass

    @property
    @abstractmethod
    def recommended_minimum_width(self) -> int:
        pass

