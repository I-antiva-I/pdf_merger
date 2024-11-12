from PyQt5.Qt import QWIDGETSIZE_MAX
from PyQt5.QtCore import QRectF, QRect, Qt, QSize
from PyQt5.QtGui import QPainter, QPen, QPaintEvent, QColor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QPushButton, QStyleOption, QStyle

from enums.component_display_mode import ComponentDisplayMode
from enums.component_state import ComponentState
from enums.display_mode import DisplayMode
from enums.svg_icon import SVGIcon
from interfaces.i_minimizable_component import IMinimizableComponent, IMinimizableComponentMeta
from managers.icon_manager import IconManager
from managers.style_manager import StyleManager


class IconButtonComponent(QPushButton, IMinimizableComponent, metaclass=IMinimizableComponentMeta):
    def __init__(self, button_text: str, button_icon: SVGIcon, is_minimized: bool = False):
        super().__init__()

        # QSvgRenderer is used for rendering SVG icon
        self.svg_renderer_default \
            = QSvgRenderer(StyleManager.modify_svg(IconManager.get_path(button_icon), ComponentState.DEFAULT))
        self.svg_renderer_hovered \
            = QSvgRenderer(StyleManager.modify_svg(IconManager.get_path(button_icon), ComponentState.HOVERED))
        self.svg_renderer_pressed \
            = QSvgRenderer(StyleManager.modify_svg(IconManager.get_path(button_icon), ComponentState.PRESSED))

        # Button text
        self.setText(button_text)
        # Size of icon
        self.icon_size = 24
        # Spacing
        self.spacing = 4
        # Cursor
        self.setCursor(Qt.PointingHandCursor)
        # Margins
        self.margin_horizontal = 4
        # Display
        self._is_minimized = is_minimized
        self.setMaximumWidth(self.recommended_minimum_width if self._is_minimized else QWIDGETSIZE_MAX)
        self.setMinimumHeight(32)

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
                + self.icon_size)

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

    def enterEvent(self, event):
        StyleManager.change_component_state(self, ComponentState.HOVERED)
        super(IconButtonComponent, self).enterEvent(event)

    def leaveEvent(self, event):
        StyleManager.change_component_state(self, ComponentState.DEFAULT)
        super(IconButtonComponent, self).leaveEvent(event)

    def mousePressEvent(self, event):
        StyleManager.change_component_state(self, ComponentState.PRESSED)
        super(IconButtonComponent, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        StyleManager.change_component_state(self, ComponentState.HOVERED)
        super(IconButtonComponent, self).mouseReleaseEvent(event)

    # </editor-fold>

    def paintEvent(self, event: QPaintEvent):
        # Create a QPainter instance for painting
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Apply default styles
        opt = QStyleOption()
        opt.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        # Calculate draw area for icon
        area_svg = QRectF(4, (self.height() - self.icon_size) // 2, self.icon_size, self.icon_size)

        # Draw icon depending on component state
        state = StyleManager.get_component_state(self)

        if state == ComponentState.PRESSED:
            self.svg_renderer_pressed.render(painter, area_svg)
        elif state == ComponentState.HOVERED:
            self.svg_renderer_hovered.render(painter, area_svg)
        else:
            self.svg_renderer_default.render(painter, area_svg)

        if not self.is_minimized:
            # Set pen color
            painter.setPen(QPen(QColor(StyleManager.themes["example"]
                                       .get(f"icon-button--{state.name.lower()}--text","#000000"))))

            # Calculate draw area for text
            area_text = QRect(4 + self.icon_size + self.spacing, 0, StyleManager.measure_text_width(self.text()), 32)

            # Draw the text with alignment
            painter.drawText(area_text, Qt.AlignLeft | Qt.AlignVCenter, self.text())
