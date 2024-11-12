import sys

from PyQt5.QtWidgets import QApplication

from components.windows.main_window import MainWindow


def main():
    application = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(application.exec_())


if __name__ == "__main__":
    main()

