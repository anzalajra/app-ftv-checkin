import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import QTimer, QTime, Qt


class CheckInSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.start_time = None  # Timer start time
        self.timer = None       # QTimer instance
        self.user_name = None   # Name of the user who checked in
        self.init_checkin_ui()  # Set up check-in UI first

    def clear_layout(self):
        """Remove the current layout (if any) to prevent overlap."""
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

    def init_checkin_ui(self):
        """Initialize the modern fullscreen Check-In UI."""
        self.clear_layout()  # Clear the current layout first
        self.setWindowTitle("Film dan Televisi Check-In")
        self.setGeometry(0, 0, 800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Set background to Fluent Design style (semi-transparent)
        self.setStyleSheet("""
            background-color: rgba(250, 250, 250, 0.8);  /* Fluent-style semi-transparent light color */
            border-radius: 16px;  /* Rounded corners for window */
        """)

        # Main Layout for Check-In
        layout_main = QVBoxLayout()

        # Title Label
        self.label_title = QLabel("Selamat Datang di Check-In")
        self.label_title.setFont(QFont("Segoe UI Variable", 24))
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("color: #000;")
        layout_main.addWidget(self.label_title)

        # Input fields with modern style
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nama Lengkap")
        self.name_input.setFont(QFont("Segoe UI Variable", 14))
        self.name_input.setStyleSheet("""
            background-color: #FFFFFF;  /* White input field */
            color: #333;  /* Input text */
            border: 1px solid #CCC;
            border-radius: 8px;
            padding: 10px;
        """)
        self.name_input.setAlignment(Qt.AlignCenter)

        self.nim_input = QLineEdit(self)
        self.nim_input.setPlaceholderText("NIM")
        self.nim_input.setFont(QFont("Segoe UI Variable", 14))
        self.nim_input.setStyleSheet("""
            background-color: #FFFFFF;
            color: #333;
            border: 1px solid #CCC;
            border-radius: 8px;
            padding: 10px;
        """)
        self.nim_input.setAlignment(Qt.AlignCenter)

        # Submit Button
        submit_button = QPushButton("Check-In")
        submit_button.setFont(QFont("Segoe UI Variable", 16))
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;  /* Windows 11 accent blue */
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #005A9E;  /* Darker blue on hover */
            }
        """)
        submit_button.clicked.connect(self.handle_checkin)

        # Input Layout
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.name_input, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.nim_input, alignment=Qt.AlignCenter)
        form_layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        layout_main.addLayout(form_layout)

        # Shutdown Button
        button_layout = QHBoxLayout()
        shutdown_button = QPushButton("Shutdown")
        shutdown_button.setFont(QFont("Segoe UI Variable", 10))
        shutdown_button.setStyleSheet("""
            QPushButton {
                background-color: #D83B01;  /* Red shutdown style */
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #A20000;  /* Darker red on hover */
            }
        """)
        shutdown_button.clicked.connect(self.shutdown_handler)
        button_layout.addStretch()
        button_layout.addWidget(shutdown_button)

        layout_main.addLayout(button_layout)
        layout_main.setContentsMargins(50, 50, 50, 50)
        self.setLayout(layout_main)

    def init_timer_ui(self):
        """Initialize a modern draggable PIP Timer UI."""
        self.clear_layout()
        self.setWindowTitle("Timer Aktif")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Name of logged-in user
        user_label = QLabel(f"Hi, {self.user_name}")
        user_label.setFont(QFont("Segoe UI Variable", 16))
        user_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_label, alignment=Qt.AlignCenter)

        # Timer Display
        self.timer_label = QLabel("Timer: 00:00:00")
        self.timer_label.setFont(QFont("Segoe UI Variable", 24))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("border: none;")
        layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setFont(QFont("Segoe UI Variable", 12))
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        logout_button.clicked.connect(self.logout_handler)
        layout.addWidget(logout_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.show()

    def handle_checkin(self):
        """Handle the user check-in logic."""
        name = self.name_input.text().strip()
        nim = self.nim_input.text().strip()

        if not name or not nim:
            self.label_title.setText("Mohon isi semua kolom!")
            self.label_title.setStyleSheet("color: red;")
            return
        
        self.user_name = name
        self.init_timer_ui()

    def logout_handler(self):
        """Handle logout."""
        self.user_name = None
        self.init_checkin_ui()

    def shutdown_handler(self):
        """Shutdown the computer on Windows."""
        os.system("shutdown /s /t 1")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckInSystem()
    app.exec_()
