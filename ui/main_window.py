import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.analytics import AnalyticsPage
from ui.daily_checkin import DailyCheckinPage
from ui.dashboard import DashboardPage
from ui.prediction import PredictionPage
from ui.profile import ProfilePage


class MainWindow(QMainWindow):
    """Main application shell for FitInsight AI."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FitInsight AI | Fitness Analytics")
        self.setMinimumSize(1120, 720)
        self.resize(1440, 900)

        self.pages = []
        self.nav_buttons = []

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        central = QWidget()
        central.setObjectName("app_root")
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(248)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(18, 28, 18, 22)
        sidebar_layout.setSpacing(9)

        brand = QLabel("FitInsight AI")
        brand.setObjectName("brand_title")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tagline = QLabel("F I T N E S S   A N A L Y T I C S")
        tagline.setObjectName("brand_subtitle")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(tagline)
        sidebar_layout.addSpacing(34)

        nav_items = [
            ("Dashboard", 0),
            ("Profile", 1),
            ("Daily Check-in", 2),
            ("Analytics", 3),
            ("ML Prediction", 4),
        ]

        for label, index in nav_items:
            button = QPushButton(label)
            button.setObjectName("nav_button")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setMinimumHeight(48)
            button.clicked.connect(
                lambda checked=False, page=index: self.change_page(page)
            )
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)

        sidebar_layout.addStretch()

        footer = QLabel("AI-POWERED FITNESS\nANALYTICS PLATFORM")
        footer.setObjectName("sidebar_footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(footer)

        root.addWidget(self.sidebar)

        # Main content
        content = QWidget()
        content.setObjectName("content_area")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.topbar = QFrame()
        self.topbar.setObjectName("topbar")
        self.topbar.setFixedHeight(76)

        topbar_layout = QHBoxLayout(self.topbar)
        topbar_layout.setContentsMargins(32, 12, 30, 12)

        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("topbar_title")
        topbar_layout.addWidget(self.page_title)
        topbar_layout.addStretch()

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("refresh_button")
        self.refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_button.clicked.connect(self.refresh_current_page)
        topbar_layout.addWidget(self.refresh_button)

        content_layout.addWidget(self.topbar)

        self.stack = QStackedWidget()
        self.stack.setObjectName("page_stack")

        self.dashboard_page = DashboardPage()
        self.profile_page = ProfilePage()
        self.checkin_page = DailyCheckinPage()
        self.analytics_page = AnalyticsPage()
        self.prediction_page = PredictionPage()

        self.pages = [
            self.dashboard_page,
            self.profile_page,
            self.checkin_page,
            self.analytics_page,
            self.prediction_page,
        ]

        for page in self.pages:
            self.stack.addWidget(page)

        content_layout.addWidget(self.stack, 1)
        root.addWidget(content, 1)

        # A successful check-in refreshes every data-driven page.
        if hasattr(self.checkin_page, "checkin_saved"):
            self.checkin_page.checkin_saved.connect(self.refresh_all_pages)

        self.change_page(0)

    def change_page(self, index):
        if not 0 <= index < len(self.pages):
            return

        self.stack.setCurrentIndex(index)
        self.page_title.setText(self.nav_buttons[index].text())

        for button_index, button in enumerate(self.nav_buttons):
            button.setChecked(button_index == index)

        page = self.pages[index]
        if hasattr(page, "refresh_data"):
            try:
                page.refresh_data()
            except Exception as error:
                print(f"Could not refresh {self.page_title.text()}: {error}")

        elif index == 1 and hasattr(page, "load_user"):
            page.load_user()

    def refresh_current_page(self):
        page = self.pages[self.stack.currentIndex()]

        if hasattr(page, "refresh_data"):
            try:
                page.refresh_data()
            except Exception as error:
                print(f"Refresh error: {error}")
        elif hasattr(page, "load_user"):
            page.load_user()

    def refresh_all_pages(self):
        for page in self.pages:
            method = getattr(page, "refresh_data", None)
            if callable(method):
                try:
                    method()
                except Exception as error:
                    print(f"Page refresh error: {error}")

        if hasattr(self.profile_page, "load_user"):
            try:
                self.profile_page.load_user()
            except Exception as error:
                print(f"Profile refresh error: {error}")

    def apply_styles(self):
        self.setStyleSheet("""
            /* FitInsight AI - unified light theme */
            QMainWindow, QWidget#app_root {
                background: #F4F7FC;
                color: #172B4D;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QWidget {
                font-family: "Segoe UI";
                color: #243653;
            }

            #sidebar {
                background: #FFFFFF;
                border-right: 1px solid #E3EAF5;
            }

            #brand_title {
                color: #142B55;
                font-size: 25px;
                font-weight: 800;
                background: transparent;
            }

            #brand_subtitle {
                color: #8796B2;
                font-size: 9px;
                font-weight: 700;
                background: transparent;
            }

            #sidebar_footer {
                color: #91A0B8;
                font-size: 9px;
                background: transparent;
            }

            QPushButton#nav_button {
                background: transparent;
                color: #71809B;
                border: none;
                border-radius: 11px;
                padding: 13px 16px;
                text-align: left;
                font-size: 13px;
                font-weight: 500;
            }

            QPushButton#nav_button:hover {
                background: #F1F5FF;
                color: #315FEA;
            }

            QPushButton#nav_button:checked {
                background: #EAF0FF;
                color: #315FEA;
                border-left: 4px solid #5277FF;
                font-weight: 700;
            }

            #content_area, #page_stack {
                background: #F4F7FC;
            }

            #topbar {
                background: #FFFFFF;
                border-bottom: 1px solid #E3EAF5;
            }

            #topbar_title {
                color: #172B55;
                font-size: 19px;
                font-weight: 700;
                background: transparent;
            }

            QPushButton#refresh_button {
                background: #FFFFFF;
                color: #315FEA;
                border: 1px solid #D7E1F3;
                border-radius: 10px;
                padding: 10px 22px;
                font-weight: 600;
            }

            QPushButton#refresh_button:hover {
                background: #EEF3FF;
                border-color: #315FEA;
            }

            QLabel#page_title {
                color: #172B55;
                font-size: 28px;
                font-weight: 750;
                background: transparent;
            }

            QLabel#description {
                color: #8291AC;
                font-size: 13px;
                background: transparent;
            }

            QFrame#card {
                background: #FFFFFF;
                border: 1px solid #E0E7F2;
                border-radius: 15px;
            }

            QFrame#card:hover {
                border: 1px solid #CFDAEE;
            }

            QLabel#card_title {
                color: #172B55;
                font-size: 15px;
                font-weight: 700;
                background: transparent;
            }

            QLabel#card_text, QLabel#date_label {
                color: #687B9B;
                font-size: 13px;
                background: transparent;
            }

            QLabel#stat_value {
                color: #172B55;
                font-size: 25px;
                font-weight: 800;
                background: transparent;
            }

            QLabel#fitness_score {
                color: #315FEA;
                font-size: 34px;
                font-weight: 800;
                background: transparent;
            }

            QLabel#prediction_result {
                color: #315FEA;
                font-size: 22px;
                font-weight: 750;
                background: transparent;
                padding: 8px 0;
            }

            QLineEdit, QComboBox, QTextEdit {
                background: #FFFFFF;
                color: #243653;
                border: 1px solid #DCE4F0;
                border-radius: 9px;
                padding: 10px 12px;
                selection-background-color: #315FEA;
                selection-color: #FFFFFF;
            }

            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #5277FF;
                background: #FFFFFF;
            }

            QLineEdit::placeholder, QTextEdit {
                color: #8A98B0;
            }

            QComboBox QAbstractItemView {
                background: #FFFFFF;
                color: #243653;
                border: 1px solid #DCE4F0;
                selection-background-color: #EAF0FF;
                selection-color: #315FEA;
                padding: 5px;
            }

            QPushButton#primary_button {
                background: #315FEA;
                color: #FFFFFF;
                border: none;
                border-radius: 9px;
                padding: 12px 20px;
                font-weight: 700;
            }

            QPushButton#primary_button:hover {
                background: #244FD1;
            }

            QPushButton#primary_button:pressed {
                background: #1D43B5;
            }

            QPushButton:disabled {
                background: #D9E1EF;
                color: #8794AA;
                border: none;
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollArea > QWidget > QWidget {
                background: transparent;
            }

            QScrollBar:vertical {
                background: #EDF1F8;
                width: 9px;
                margin: 2px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: #C4D0E3;
                min-height: 30px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #9EAFCA;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }

            QMessageBox {
                background: #FFFFFF;
            }

            QMessageBox QLabel {
                color: #243653;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("FitInsight AI")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
