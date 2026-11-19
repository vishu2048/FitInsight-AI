import sys

from PySide6.QtWidgets import QApplication

from database import create_tables
from ui.main_window import MainWindow


def main():

    # Create database tables
    create_tables()

    # Start Qt application
    app = QApplication(sys.argv)

    app.setApplicationName("FitInsight AI")

    # Create main window
    window = MainWindow()

    window.show()

    # Start application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()