from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, \
    QDragMoveEvent, QDragLeaveEvent
from PyQt5.QtWidgets import QSizePolicy, QFrame, QVBoxLayout, QGridLayout, QScrollArea, QWidget

from components.merge.document_component import DocumentComponent
from enums.component_state import ComponentState
from enums.display_mode import DisplayMode
from enums.message_type import MessageType
from interfaces.i_adaptive_component import IAdaptiveComponent, IAdaptiveComponentMeta
from interfaces.i_minimizable_component import IMinimizableComponent
from managers.message_manager import MessageManager
from managers.style_manager import StyleManager
from viewmodels.merge_viewmodel import DocumentItem

from typing import Type


class AdaptivePanelComponent(QFrame, IAdaptiveComponent, metaclass=IAdaptiveComponentMeta):

    def __init__(self, inner_component_type: Type[QWidget], display_mode: DisplayMode = DisplayMode.LIST):
        super().__init__()

        # Base layout of component
        base_layout = QVBoxLayout()
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(0)
        base_layout.setAlignment(Qt.AlignTop)

        # Container layout
        self.container_layout = QGridLayout()
        self.container_layout.setContentsMargins(8, 8, 8, 8)
        self.container_layout.setSpacing(8)
        self.container_layout.setAlignment(Qt.AlignTop)

        # Container for inner components
        self.component_container = QFrame()
        self.component_container.setLayout(self.container_layout)
        self.component_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # References to inner components
        self.inner_components: List[inner_component_type] = list()

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.component_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Settings
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        base_layout.addWidget(self.scroll_area)
        self.setLayout(base_layout)

        #
        self._display_mode = display_mode
        self.grid_column_count = 4
        self.list_column_count = 1
        self.grid_preferred_column_width = 168
        self.setAcceptDrops(True)
        self.last_reached_inner_component: inner_component_type = None
        self.inner_component_type = inner_component_type

    # <editor-fold desc="[+] Properties">

    @property
    def number_of_inner_components(self) -> int:
        return len(self.inner_components)

    @property
    def display_mode(self) -> DisplayMode:
        return self._display_mode

    @display_mode.setter
    def display_mode(self, value: DisplayMode) -> None:
        if self._display_mode != value:
            self._display_mode = value
            self.reshape_grid()
            self.rearrange_content()

    # </editor-fold>

    # <editor-fold desc="[+] Layout manipulation">

    def rearrange_content(self, should_rearrange_inner_components: bool = True):
        #
        self.detach_all_inner_components()
        #
        if should_rearrange_inner_components:
            for component in self.inner_components:
                if isinstance(component, IAdaptiveComponent):
                    component.display_mode = self.display_mode
        #
        self.attach_all_inner_components()

    def attach_inner_component(self, inner_component: QWidget, index: int = None) -> None:
        if index is None:
            index = self.number_of_inner_components - 1

        row = index // (self.grid_column_count if self.display_mode == DisplayMode.GRID else self.list_column_count)
        column = index % (self.grid_column_count if self.display_mode == DisplayMode.GRID else self.list_column_count)

        self.container_layout.addWidget(inner_component, row, column, 1, 1)
        inner_component.setParent(self.component_container)
        inner_component.setVisible(True)

    def detach_inner_component(self, inner_component: QWidget) -> None:
        self.container_layout.removeWidget(inner_component)
        inner_component.setParent(None)
        inner_component.setVisible(False)

    def attach_all_inner_components(self):
        for index, component in enumerate(self.inner_components):
            self.attach_inner_component(component, index)

    def detach_all_inner_components(self):
        for component in self.inner_components:
            self.detach_inner_component(component)

    def reshape_grid(self):
        for column in range(self.container_layout.columnCount()):
            self.container_layout.setColumnStretch(column, 0)

        if self.display_mode == DisplayMode.GRID:
            for column in range(self.grid_column_count):
                self.container_layout.setColumnStretch(column, 1)

        else:
            for column in range(self.list_column_count):
                self.container_layout.setColumnStretch(column, 1)

    def display_as_grid(self):
        self.display_mode = DisplayMode.GRID

    def display_as_list(self):
        self.display_mode = DisplayMode.LIST

    def resizeEvent(self, event):
        super().resizeEvent(event)

        work_width = self.width()
        possible_grid_column_count = work_width // (self.grid_preferred_column_width + 8)

        if self.grid_column_count != possible_grid_column_count:
            self.grid_column_count = possible_grid_column_count
            self.reshape_grid()
            self.rearrange_content(False)

    # </editor-fold>

    # <editor-fold desc="[+] Drag and drop">

    def check_reached_component(self, coordinate_x: int, coordinate_y: int,
                                component_width: int, component_height: int) -> int:

        margin = 8
        spacing = 8

        reached_column = (coordinate_x - margin) // (component_width + spacing)
        reached_row = (coordinate_y - margin ) // (component_height + spacing)

        column_count = self.container_layout.columnCount()
        reached_index = min(max(0, reached_row * column_count + reached_column), self.number_of_inner_components - 1)

        return reached_index

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        # Source
        event_source = event.source()

        # Check type
        if not isinstance(event_source, self.inner_component_type):
            return

        # Remember dragged component
        self.last_reached_inner_component = event_source

        event.accept()

        self.on_drag_enter_event_competed()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        event.accept()

        self.on_drag_leave_event_competed()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        # Source
        event_source = event.source()

        # Check type
        if not isinstance(event_source, QWidget):
            return

        index = self.check_reached_component(event.pos().x(), event.pos().y(),
                                             event_source.width(), event_source.height())

        previous_component = self.last_reached_inner_component
        self.last_reached_inner_component = self.inner_components[index]

        event.accept()

        self.on_drag_move_event_competed(previous_component)

    def dropEvent(self, event: QDropEvent) -> None:
        # Assign indexes
        source_component = event.source()
        destination_component = self.last_reached_inner_component

        if source_component == destination_component:
            self.on_drop_event_competed(-1, -1)
            return

        # Swap
        destination_index = self.inner_components.index(destination_component)
        source_index = self.inner_components.index(source_component)

        self.inner_components.remove(source_component)
        self.inner_components.insert(destination_index, source_component)

        # Swap
        self.detach_all_inner_components()
        self.attach_all_inner_components()

        event.accept()

        self.on_drop_event_competed(source_index, destination_index)

    def on_drag_enter_event_competed(self):
        pass

    def on_drag_leave_event_competed(self):
        pass

    def on_drag_move_event_competed(self, previous_component):
        pass

    def on_drop_event_competed(self, source_index: int, destination_index: int):
        pass

    # </editor-fold>
