from PyQt5.QtWidgets import QSizePolicy, QFrame, QHBoxLayout, QLabel

from components.core.icon_button_component import IconButtonComponent
from enums.message_type import MessageType
from enums.svg_icon import SVGIcon
from managers.message_manager import MessageManager


class ControlPanelComponent(QFrame):
    def __init__(self):
        super().__init__()

        self.button_add_file = IconButtonComponent("Add File", SVGIcon.FILE_PLUS)
        self.label_document_number = QLabel("Documents: 0")
        button_list_view = IconButtonComponent("List View", SVGIcon.LIST)
        button_grid_view = IconButtonComponent("Grid View", SVGIcon.GRID)

        self.setProperty("class", "control_panel")
        self.button_add_file.setProperty("class", "control_panel__button_add_file")
        self.label_document_number.setProperty("class", "control_panel__label_document_number")
        button_list_view.setProperty("class", "control_panel__button_list_view")
        button_grid_view.setProperty("class", "control_panel__button_grid_view")

        self.label_document_number.setContentsMargins(4, 4, 4, 4)
        self.label_document_number.setMinimumHeight(32)

        self.button_add_file.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.label_document_number.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        button_list_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        button_grid_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        layout.addWidget(self.label_document_number)
        layout.addWidget(self.button_add_file)
        layout.addWidget(button_list_view)
        layout.addWidget(button_grid_view)

        button_list_view.clicked.connect(lambda: MessageManager.send(MessageType.MERGE_VIEW__DISPLAY_AS_LIST))
        button_grid_view.clicked.connect(lambda: MessageManager.send(MessageType.MERGE_VIEW__DISPLAY_AS_GRID))

        self.setLayout(layout)

    def set_number_of_documents(self, number_of_documents: int):
        self.label_document_number.setText(f"Documents: {number_of_documents}")
