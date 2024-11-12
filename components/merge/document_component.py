import io

import fitz
from PIL import Image
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QPainter, QDrag, QPixmap, QBitmap, QImage
from PyQt5.QtWidgets import QFrame, QLabel, QSizePolicy, QGridLayout, QVBoxLayout

from components.core.checkbox_component import CheckboxComponent
from components.core.icon_button_component import IconButtonComponent
from enums.component_state import ComponentState
from enums.display_mode import DisplayMode
from enums.message_type import MessageType
from enums.svg_icon import SVGIcon
from interfaces.i_adaptive_component import IAdaptiveComponent, IAdaptiveComponentMeta
from managers.message_manager import MessageManager
from managers.style_manager import StyleManager
from viewmodels.merge_viewmodel import DocumentItem


class DocumentComponent(QFrame, IAdaptiveComponent, metaclass=IAdaptiveComponentMeta):

    def __init__(self, document_item: DocumentItem, display_mode: DisplayMode = DisplayMode.LIST):
        super().__init__()

        # Assigned DocumentItem
        self.document_item = document_item

        # Inner components
        self.label_document_index = QLabel(str(self.document_item.document_index+1))
        self.label_document_name = QLabel(self.document_item.document_name)
        self.checkbox_is_included = CheckboxComponent()
        self.icon_button_remove = IconButtonComponent("Remove", SVGIcon.CIRCLE_REMOVE)
        self.frame_preview = QFrame()

        # Style classes
        self.setProperty("class", "document")
        self.label_document_index.setProperty("class", "document__index")
        self.label_document_name.setProperty("class", "document__name")
        self.checkbox_is_included.setProperty("class", "document__checkbox")
        self.icon_button_remove.setProperty("class", "document__button")
        self.frame_preview.setProperty("class", "document__frame")

        # Layout
        layout = QGridLayout()
        self.setLayout(layout)
        self.layout().setContentsMargins(8, 8, 8, 8)
        self.layout().setSpacing(8)

        #
        #self.frame_preview.setMinimumSize(112, 112)

       #

        # Misc
        self.label_document_index.setMinimumSize(32, 32)
        self.label_document_name.setMinimumHeight(32)
        #self.setMinimumHeight(48)

        self.label_document_index.setContentsMargins(4, 4, 4, 4)
        self.label_document_name.setContentsMargins(4, 4, 4, 4)

        self.label_document_index.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.label_document_name.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.checkbox_is_included.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.icon_button_remove.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)

        self.icon_button_remove.clicked.connect(self.on_button_remove_clicked)
        self.checkbox_is_included.stateChanged.connect(self.on_checkbox_is_included_clicked)

        self.generate_preview()
        self._display_mode = display_mode
        self.attach_all_inner_components()

        self.label_document_index.setCursor(Qt.PointingHandCursor)
        self.label_document_name.setCursor(Qt.PointingHandCursor)
        self.frame_preview.setCursor(Qt.PointingHandCursor)

    def generate_preview(self):
        pdf_document = fitz.open(self.document_item.document_path)
        first_page = pdf_document[0]
        width, height = first_page.rect.width, first_page.rect.height

        # Render the first page to a pixmap
        pix = first_page.get_pixmap(dpi=72)  # 72 DPI is generally sufficient for thumbnails

        # Convert the pixmap to bytes and open with PIL
        img = Image.open(io.BytesIO(pix.tobytes("jpg")))

        limit_w = 112
        limit_h = 112

        scale_w = limit_w / width
        scale_h = limit_h / height

        scale = min(scale_h, scale_w)

        good_w = min(limit_w, int(round(scale * width)))
        good_h = min(limit_w, int(round(scale * height)))

        # Resize the image to 128x128
        img = img.resize((int(good_w), int(good_h)))

        print(">>>", good_w, good_h, scale*height)

        # Convert the PIL image to QImage
        img_data = img.convert("RGBA")
        qimage = QImage(img_data.tobytes(), int(img_data.width), int(img_data.height), QImage.Format_RGBA8888)

        label = QLabel()
        pixmap = QPixmap.fromImage(qimage)
        label.setPixmap(pixmap)

        # preview
       # self.frame_preview.setStyleSheet("background: #6F4E37; border: 2px solid #4D3120; border-radius: 4px;")
        label.setProperty("class", "document__preview")
      #  label.setStyleSheet("background: #FFDEAD; border: 0px solid #4D3120; border-radius: 4px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)
        layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.frame_preview.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

       # self.setAcceptDrops(True)


    # <editor-fold desc="[+] Properties">

    @property
    def document_index(self) -> int:
        return self.document_item.document_index

    @document_index.setter
    def document_index(self, value: int) -> None:
        self.document_item.document_index = value

    @property
    def document_name(self) -> str:
        return self.document_item.document_name

    @property
    def document_is_included(self) -> bool:
        return self.document_item.document_is_included

    @document_is_included.setter
    def document_is_included(self, value: bool) -> None:
        self.document_item.document_is_included = value

    @property
    def display_mode(self) -> DisplayMode:
        return self._display_mode

    @display_mode.setter
    def display_mode(self, value: DisplayMode) -> None:
        if self._display_mode != value:
            self._display_mode = value
            self.rearrange_content()

    # </editor-fold>

    # <editor-fold desc="[+] Layout manipulations">

    def rearrange_content(self) -> None:
        self.detach_all_inner_components()
        self.attach_all_inner_components()

    def attach_all_inner_components(self):
        if self.display_mode == DisplayMode.LIST:
            # Hide preview
            self.frame_preview.setVisible(False)

            # Minimize components
            self.icon_button_remove.is_minimized = False
            self.checkbox_is_included.is_minimized = False

            # Place components
            self.layout().addWidget(self.label_document_index, 0, 0)
            self.layout().addWidget(self.label_document_name, 0, 1)
            self.layout().addWidget(self.checkbox_is_included, 0, 2)
            self.layout().addWidget(self.icon_button_remove, 0, 3)

            # Adjust self
            self.setMinimumSize(96, 48)
            self.setMaximumHeight(48)

        elif self.display_mode == DisplayMode.GRID:
            # Place components
            self.icon_button_remove.is_minimized = True
            self.checkbox_is_included.is_minimized = True

            # Place components
            self.layout().addWidget(self.icon_button_remove, 0, 3, 1, 1)
            self.layout().addWidget(self.label_document_index, 1, 3, 1, 1)
            self.layout().addWidget(self.checkbox_is_included, 2, 3, 1, 1)
            self.layout().addWidget(self.label_document_name, 3, 0, 1, 4)
            self.layout().addWidget(self.frame_preview, 0, 0, 3, 3)

            # Show preview
            self.frame_preview.setVisible(True)

            # Adjust self
            self.setMinimumSize(168, 168)
            self.setMaximumHeight(168)
            #self.setMaximumWidth(168)

        else:
            raise ValueError(f"Unsupported display mode: '{self.display_mode}'")

    def detach_all_inner_components(self):
        self.layout().removeWidget(self.label_document_index)
        self.layout().removeWidget(self.label_document_name)
        self.layout().removeWidget(self.checkbox_is_included)
        self.layout().removeWidget(self.icon_button_remove)
        self.layout().removeWidget(self.frame_preview)

    # </editor-fold>

    def update_document_index(self, new_document_index: int):
        self.document_index = new_document_index
        self.label_document_index.setText(str(new_document_index+1))

    def on_button_remove_clicked(self):
        MessageManager.send(MessageType.DOCUMENT_REMOVE_CLICKED, document_component=self)

        # self.place_inner_components(DisplayMode.LIST_DOCUMENT_COMPONENT)
        # if self.display_mode == DisplayMode.LIST:

        #       self.rearrange_inner_components(DisplayMode.GRID)
        #   else:
        #         self.rearrange_inner_components(DisplayMode.LIST)
        #

    def on_checkbox_is_included_clicked(self, new_state: int):
        new_state_as_bool: bool = (new_state != 0)
        self.document_is_included = new_state_as_bool

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            # QDrag object to manage the drag-and-drop operation
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            # Create an empty pixmap with the same dimensions as the widget
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.transparent)  # Fill with transparency

            # Set up a painter to draw the widget's content with opacity
            painter = QPainter(pixmap)
            painter.setOpacity(0.5)  # Adjust opacity
            self.render(painter)  # Draw the widget's content
            painter.end()

            # Create a mask with rounded corners
            mask = QBitmap(pixmap.size())
            mask.fill(Qt.color0)  # Fill the mask with transparent color
            painter = QPainter(mask)
            painter.setRenderHint(QPainter.Antialiasing)  # Smooth edges
            radius = 4  # Adjust radius for rounded corners
            painter.setBrush(Qt.color1)  # Set brush to solid for visible area
            painter.drawRoundedRect(pixmap.rect(), radius, radius)
            painter.end()

            # Apply the rounded mask to the pixmap
            pixmap.setMask(mask)

            # Set the modified pixmap as the drag image
            drag.setPixmap(pixmap)
            drag.exec_(Qt.MoveAction)




   # def enterEvent(self, e):
    #    print("hi, I am", self.label_document_name.text())
    """
    def place_inner_components(self, display_mode: DisplayMode):
        if display_mode == display_mode.GRID_VIEW:
            sub_layout = QGridLayout()

            v = QFrame()
            v.setStyleSheet("background: #f5f5f5; border: none; border-radius: 4px;")
            v.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            v.setMinimumWidth(32)
            v.setMinimumHeight(32)




            self.icon_button_remove.setFixedSize(32, 32)
            self.checkbox_is_included.setFixedSize(32, 32)

            self.setFixedSize(168, 168)

            self.layout().addLayout(sub_layout)
            self.label_document_name.setText("Long long long long long name")

        #    print(StyleManager.measure_text_width("Long long long long long name"))
         #   print(self.label_document_name.sizeHint())
            l = ((175-8) / (221)) * len("LIST_DOCUMENT_COMPONENT")
          #  print(l)
        #    print("!!", StyleManager.measure_text_width("..."))
            k = int(l)-4
            #print("LIST_DOCUMENT_COMPONENT"[:k]+"...")
            self.label_document_name.setText("LIST_DOCUMENT_COMPONENT"[:k]+"...")


            sub_layout.setContentsMargins(8, 8, 8, 8)
            sub_layout.setSpacing(8)


        elif display_mode == display_mode.LIST_VIEW:
            while self.layout().count():
                item = self.layout().takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

            sub_layout = QHBoxLayout()

            sub_layout.addWidget(self.label_document_index)
            sub_layout.addWidget(self.label_document_name)
            sub_layout.addWidget(self.checkbox_is_included)
            sub_layout.addWidget(self.icon_button_remove)

            self.layout().addLayout(sub_layout)

            sub_layout.setContentsMargins(8, 8, 8, 8)
            sub_layout.setSpacing(8)

            # Initialize GridLayout
           # self.layout().deleteLater()
           # grid_layout = QHBoxLayout()
          # # self.setLayout(grid_layout)

        #    grid_layout.setParent(self)


            print(self.label_document_index.parent())
            print(self)

            # Clear the existing layout if any
            if self.layout() is not None:
                while self.layout().count() > 0:
                    item = self.layout().takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)  # Detach widget without deleting it

                # Delete the layout to clear the layout structure


                # Set an empty temporary layout to ensure deletion is processed
               # self.setLayout(QHBoxLayout())
            self.layout().deleteLater()
            print(self.layout().parent())
            self.layout().setParent(None)

            # Now, set up the new layout
            new_layout = QGridLayout()

            # Add widgets to the new layout

#
            # Set the new layout to the widget
            self.setLayout(new_layout)

            # Adjust minimum height if needed
            self.setMinimumHeight(323)


     #       print(self.label_document_index.parent())
            print(self.label_document_index.isVisible())
#
            #self.label_document_index.setParent(self)
          #  self.label_document_name.setParent(self)
         #   self.checkbox_is_included.setParent(self)
         # #  self.icon_button_remove.setParent(self)

          #  self.label_document_index.setVisible(True)
      #      self.label_document_name.setVisible(True)
     #       self.checkbox_is_included.setVisible(True)
        #    self.icon_button_remove.setVisible(True)

        #    self.update()

            print(self.layout())

"""


