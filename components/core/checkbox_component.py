from PyQt5.Qt import QWIDGETSIZE_MAX
from PyQt5.QtCore import QRectF, QRect, Qt, QSize
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent, QFont, QFontMetrics
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QCheckBox, QStyleOption, QStyle, QSizePolicy

from enums.component_state import ComponentState
from enums.svg_icon import SVGIcon
from interfaces.i_minimizable_component import IMinimizableComponent, IMinimizableComponentMeta
from managers.icon_manager import IconManager
from managers.style_manager import StyleManager


class CheckboxComponent(QCheckBox, IMinimizableComponent, metaclass=IMinimizableComponentMeta):
    def __init__(self, checkbox_text: str = "Included", initial_state: bool = True, is_minimized: bool = False):
        super().__init__()

        # Load the SVG file using QSvgRenderer
        self.svg_renderer_checked \
            = QSvgRenderer(StyleManager.modify_svg(IconManager.
                                                   get_path(SVGIcon.CHECKBOX_INDICATOR), ComponentState.CHECKED))
        self.svg_renderer_unchecked \
            = QSvgRenderer(StyleManager.modify_svg(IconManager.
                                                   get_path(SVGIcon.CHECKBOX_INDICATOR), ComponentState.UNCHECKED))

        # Initial state
        self.setChecked(initial_state)
        # Checkbox text
        self.setText(checkbox_text)
        # Size of indicator (checkbox)
        self.indicator_size = 24
        # Margins
        self.margin_horizontal = 4
        # Spacing
        self.spacing = 4
        # Display
        self._is_minimized = is_minimized
        self.setMaximumWidth(self.recommended_minimum_width if self._is_minimized else QWIDGETSIZE_MAX)
        self.setMinimumWidth(32)
        self.setMinimumHeight(32)
        # Cursor
        self.setCursor(Qt.PointingHandCursor)

    # <editor-fold desc="[+] Properties">

    @property
    def is_minimized(self) -> bool:
        return self._is_minimized

    @is_minimized.setter
    def is_minimized(self, new_value: bool) -> None:
        if self._is_minimized != new_value:
            # Set to a new value
            self._is_minimized = new_value
            self.setMaximumWidth(self.recommended_minimum_width if self._is_minimized else QWIDGETSIZE_MAX)
            self.updateGeometry()

    @property
    def recommended_minimum_width(self) -> int:
        return ((StyleManager.measure_text_width(self.text()) + self.spacing)
                * int(not self.is_minimized)
                + (self.margin_horizontal * 2)
                + self.indicator_size)

    # </editor-fold>

    # <editor-fold desc="[+] Size hints">

    def sizeHint(self):
        # Return a QSize with preferred dimensions
        return QSize(self.recommended_minimum_width, 32)

    def minimumSizeHint(self):
        # Return a QSize with minimum dimensions
        return QSize(self.recommended_minimum_width, 32)

    # </editor-fold>

    # <editor-fold desc="[+] Mouse events">
    def mousePressEvent(self, event: QMouseEvent):

        if event.button() == Qt.LeftButton:
            print(f"Left Button Pressed at position: {event.pos()}")
        elif event.button() == Qt.RightButton:
            print(f"Right Button Pressed at position: {event.pos()}")

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        # Check if the click is within the extended area (including margins)
        if event.button() == Qt.LeftButton: #and (not extended_rect.contains(event.pos())) and self.rect().contains(event.pos()):
            self.setChecked(not self.isChecked())

       # super().mouseReleaseEvent(event)

    # </editor-fold>

    def paintEvent(self, event):
        # Create a QPainter instance for painting
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Apply default styles
        opt = QStyleOption()
        opt.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        # Calculate draw area for indicator
        area_svg = QRectF(4, (self.height() - self.indicator_size) // 2, self.indicator_size, self.indicator_size)

        # If the checkbox is checked, draw the SVG icon
        if self.isChecked():
            self.svg_renderer_checked.render(painter, area_svg)
        else:
            self.svg_renderer_unchecked.render(painter, area_svg)

        if not self.is_minimized:
            # Set pen color
            painter.setPen(QPen(Qt.black))

            # Calculate draw area for text
            area_text = QRect(4 + self.indicator_size + self.spacing, 0,
                              StyleManager.measure_text_width(self.text()), 32)

            # Draw the text with vertical and horizontal centering
            painter.drawText(area_text, Qt.AlignLeft | Qt.AlignVCenter, self.text())
