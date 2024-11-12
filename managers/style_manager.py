import json
from typing import Dict
from xml.etree import ElementTree

from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QFontDatabase, QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget

from enums.component_state import ComponentState
from managers.path_manager import PathManager


class StyleManager:
    themes: Dict[str, Dict[str, str]] = {}
    @classmethod
    def load_themes(cls):
        with open("assets/json/themes.json", 'r') as f:
            colors = json.load(f)
            #print(colors)
            #print(type(colors))
            #print(colors["example"])
            cls.themes = colors

    @classmethod
    def load_styles(cls, component: QWidget) -> None:
        styles = open(PathManager.path_to_stylesheet(), "r").read()
        component.setStyleSheet(styles)

    @classmethod
    def measure_text_width(cls, text: str) -> int:
        font = QFont("Roboto", 16)
        font.setPixelSize(16)
        font.setWeight(QFont.Weight.Medium)

        # Create a QFontMetrics object
        font_metrics = QFontMetrics(font)

        # Calculate the width of the text string
        return font_metrics.horizontalAdvance(text)

    @classmethod
    def change_component_state(cls, component: QWidget, component_state: ComponentState):
        component.setProperty("state", component_state.name)
        component.style().polish(component)

    @classmethod
    def get_component_state(cls, component: QWidget) -> ComponentState:
        state: ComponentState = ComponentState[component.property("state")] if component.property("state") is not None \
            else ComponentState.DEFAULT

        return state

    @classmethod
    def modify_svg(cls, svg_path, component_state: ComponentState = ComponentState.DEFAULT) -> QByteArray:
        tree = ElementTree.parse(svg_path)
        root = tree.getroot()

        # Modify the SVG content (as an example, change fill='RED' to 'blue')
        namespace = {'svg': 'http://www.w3.org/2000/svg'}
        elements = root.findall(".//*[@class='theme-dependent']", namespaces=namespace)

        for element in elements:
            fill_key = element.get("fill", None)

            if fill_key.__contains__("{state}"):
                fill_key = fill_key.replace("{state}", component_state.name.lower())

            fill_color = cls.themes["example"].get(fill_key, "#000000")
            element.set("fill", fill_color)

            #print(fill_key, fill_color, element.get("fill", None))

        # Convert the ElementTree object back to a string
        svg_data = ElementTree.tostring(root, encoding='utf-8').decode('utf-8')

        # Convert the SVG data to QByteArray for QSvgRenderer
        byte_array = QByteArray(svg_data.encode('utf-8'))

        return byte_array

    @classmethod
    def load_fonts(cls) -> None:
        for font_folder in PathManager.path_to_fonts().iterdir():
            for file in font_folder.iterdir():
                if file.suffix == ".ttf":
                    QFontDatabase.addApplicationFont(str(file))
