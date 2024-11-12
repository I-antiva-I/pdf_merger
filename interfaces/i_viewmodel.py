from abc import abstractmethod, ABCMeta

from PyQt5.QtCore import QObject


class IViewModelMeta(ABCMeta, type(QObject)):
    """
    A metaclass that combines the `ABCMeta` for defining abstract base class with
    `type(QObject)` to enable QObject inheritance.
    """
    pass


class IViewModel(metaclass=IViewModelMeta):
    """
    An interface for `viewmodels`. The interface enforces the implementation of a `model` and 'shared_data'
    properties in derived classes.
    """

