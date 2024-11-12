from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, \
    QDragMoveEvent, QDragLeaveEvent
from PyQt5.QtWidgets import QSizePolicy, QFrame, QVBoxLayout, QGridLayout, QScrollArea

from components.core.adaptive_panel_component import AdaptivePanelComponent
from components.merge.document_component import DocumentComponent
from enums.component_state import ComponentState
from enums.display_mode import DisplayMode
from enums.message_type import MessageType
from managers.message_manager import MessageManager
from managers.style_manager import StyleManager
from viewmodels.merge_viewmodel import DocumentItem


class DocumentPanelComponent(AdaptivePanelComponent):
    def __init__(self):
        super().__init__(DocumentComponent)

        self.setProperty("class", "document__panel")
        self.component_container.setProperty("class", "document_panel__container")
        self.scroll_area.setProperty("class", "document_panel__scroll_area")

        MessageManager.subscribe(MessageType.MERGE_VIEWMODEL__DOCUMENT_REMOVED, self, self.update_document_indexes)

    def add_document_component(self, document_item: DocumentItem):
        document_component = DocumentComponent(document_item, self.display_mode)
        self.inner_components.append(document_component)
        self.attach_inner_component(document_component)

    def remove_document_component(self, document_component: DocumentComponent):
        self.inner_components.remove(document_component)
        MessageManager.send(MessageType.MERGE_VIEW__DOCUMENT_REMOVED, document_index=document_component.document_index)
        self.rearrange_content(False)
        document_component.deleteLater()

    def update_document_indexes(self, starting_index: int = 0):
        for index in range(starting_index, self.number_of_inner_components):
            w: DocumentComponent = self.inner_components[index]
            w.update_document_index(index)

    def on_drag_enter_event_competed(self):
        StyleManager.change_component_state(self.last_reached_inner_component, ComponentState.HOVERED)

    def on_drag_leave_event_competed(self):
        StyleManager.change_component_state(self.last_reached_inner_component, ComponentState.DEFAULT)

    def on_drag_move_event_competed(self, previous_component):
        StyleManager.change_component_state(previous_component, ComponentState.DEFAULT)
        StyleManager.change_component_state(self.last_reached_inner_component, ComponentState.HOVERED)

    def on_drop_event_competed(self, source_index: int, destination_index: int):
        StyleManager.change_component_state(self.last_reached_inner_component, ComponentState.DEFAULT)

        if destination_index == source_index:
            return

        if destination_index < source_index:
            destination_index, source_index = source_index, destination_index

        for i in range(source_index, destination_index + 1):
            w: DocumentComponent = self.inner_components[i]
            w.update_document_index(i)

        MessageManager.send(MessageType.MERGE_VIEW__DOCUMENTS_REORDERED, source_index, destination_index)