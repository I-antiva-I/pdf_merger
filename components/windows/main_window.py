import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QFrame, QVBoxLayout, QPushButton

from managers.message_manager import MessageManager, MessageType

from managers.style_manager import StyleManager
from viewmodels.merge_viewmodel import MergeViewModel
from views.merge_view import MergeView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set theme
        self.setProperty("class", "theme--chocolate")

        # Load themes, fonts, and styles
        StyleManager.load_themes()
        StyleManager.load_fonts()
        StyleManager.load_styles(self)

        # Models

        # Viewmodels
        merge_viewmodel = MergeViewModel()

        # Views
        merge_view = MergeView(merge_viewmodel)

        # Tabs

        # Central widget
        central_frame = QFrame()
        central_frame.setLayout(QVBoxLayout())
        central_frame.layout().addWidget(merge_view)
        central_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_frame)

        # Window
       # self.resize(int(640*1.125), int(480*1.125))
        self.resize(712, 534)
        self.setWindowTitle("PDF Merger")




        # Fast CSS testing
        """
        refresh_stylesheets = QPushButton("CSS")
        refresh_stylesheets.clicked.connect(lambda: [StyleManager.load_themes(), StyleManager.load_styles(self)])
        central_frame.layout().addWidget(refresh_stylesheets)
        
        MessageManager.subscribe(MessageType.DEFAULT, self, self.hello)
        """