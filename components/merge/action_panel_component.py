from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QSizePolicy, QFrame, QLabel, \
    QLineEdit, QGridLayout

from components.core.icon_button_component import IconButtonComponent
from enums.message_type import MessageType
from enums.svg_icon import SVGIcon
from managers.message_manager import MessageManager


class ActionPanelComponent(QFrame):
    def __init__(self):
        super().__init__()

        button = IconButtonComponent("Merge", SVGIcon.LIGHTNING)
        label = QLabel("Merged PDF name")
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Input new filename here")

        self.setProperty("class", "action_panel")
        self.input_line.setProperty("class", "action_panel__input")
        label.setProperty("class", "action_panel__label")
        button.setProperty("class", "action_panel__button")

        palette = self.input_line.palette()
        palette.setColor(QPalette.PlaceholderText, QColor("#A9A9A9"))
        self.input_line.setPalette(palette)

        label.setContentsMargins(4, 4, 4, 4)
        label.setMinimumHeight(32)

        self.setLayout(QGridLayout())
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.layout().setSpacing(8)
        self.layout().setContentsMargins(8, 8, 8, 8)

        self.layout().addWidget(label, 0, 0, 1, 1)
        self.layout().addWidget(self.input_line, 0, 1, 1, 2)
        self.layout().addWidget(button, 0, 3, 1, 1)

        button.setSizePolicy(QSizePolicy.Preferred , QSizePolicy.Maximum)
        self.input_line.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        label.setSizePolicy(QSizePolicy.Preferred , QSizePolicy.Maximum)

        button.clicked.connect(self.on_button_merge_clicked)

    def on_button_merge_clicked(self):
        MessageManager.send(MessageType.ACTION_MERGE_CLICKED, pdf_filename=self.input_line.text())