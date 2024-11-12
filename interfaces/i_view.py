from abc import abstractmethod, ABCMeta

from PyQt5.QtWidgets import QWidget

from interfaces.i_viewmodel import IViewModel


class IViewMeta(ABCMeta, type(QWidget)):
    """
    A metaclass that combines the `ABCMeta` for defining abstract base class with
    `type(QWidget)` to enable QWidget inheritance.
    """
    pass


class IView(metaclass=IViewMeta):
    """
    An interface for `views`. The interface enforces the implementation of a `viewmodel` property in derived classes.
    """

    @property
    @abstractmethod
    def viewmodel(self) -> IViewModel:
        """
        Abstract getter for the `viewmodel`.
        """
        pass

    @viewmodel.setter
    @abstractmethod
    def viewmodel(self, value: IViewModel):
        """
        Abstract setter for the `viewmodel`.
        """
        pass
