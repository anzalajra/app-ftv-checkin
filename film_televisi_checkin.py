import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt


class CheckInSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.start_time = None
        self.timer = None
        self.user_name = None
        self.init_checkin_ui()

    def clear_layout(self):
        """Remove the current layout (if any) to prevent overlap."""
        if self.layout() is not None:
            QWidget().setLayout(self.layout())

    def init_checkin_ui(self):
        """Initialize the fullscreen Check-In UI (now with improved UI/UX)."""
        self.clear_layout()
        self.setWindowTitle("Film dan Televisi Check-In")
        self.setGeometry(0, 0, 800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Fullscreen without window border

        # Main Layout
        layout_main = QVBoxLayout()

        # Title
        self.label_title = QLabel("Selamat Datang! Silakan Check-In")
        self.label_title.setFont(QFont("Segoe UI Variable", 20))
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("color: #2b2b2b;")  # Dark-gray text
        layout_main.addWidget(self.label_title)

        # Input Fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nama Lengkap")
        self.name_input.setFont(QFont("Segoe UI Variable", 14))
        self.name_input.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 10px;
            padding: 8px;
        """)
        self.name_input.setAlignment(Qt.AlignCenter)

        self.nim_input = QLineEdit()
        self.nim_input.setPlaceholderText("NIM")
        self.nim_input.setFont(QFont("Segoe UI Variable", 14))
        self.nim_input.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 10px;
            padding: 8px;
        """)
        self.nim_input.setAlignment(Qt.AlignCenter)

        submit_button = QPushButton("Check-In")
        submit_button.setFont(QFont("Segoe UI Variable", 16))
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;  /* Fluent blue */
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        submit_button.clicked.connect(self.handle_checkin)

        # Add Input to Layout
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.nim_input)
        form_layout.addWidget(submit_button, alignment=Qt.AlignCenter)
        layout_main.addLayout(form_layout)

        # Shutdown button (bottom-right)
        shutdown_button = QPushButton("Shutdown")
        shutdown_button.setFont(QFont("Segoe UI Variable", 10))
        shutdown_button.setStyleSheet("""
            QPushButton {
                background-color: #d83b01;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 10px;
            }
            QPushButton:hover {
                background-color: #a20000;
            }
        """)
        shutdown_button.clicked.connect(self.shutdown_handler)

        shutdown_layout = QHBoxLayout()
        shutdown_layout.addStretch()
        shutdown_layout.addWidget(shutdown_button)
        layout_main.addLayout(shutdown_layout)

        self.setLayout(layout_main)
        self.showFullScreen()

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

    def init_timer_ui(self):
        """Initialize the Timer UI (minimal and modern)."""
        self.clear_layout()
        self.setWindowTitle("Timer Aktif")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Draggable and above other windows

        # Timer UI Layout
        layout = QVBoxLayout()

        # User Name
        user_label = QLabel(f"Hi, {self.user_name}")
        user_label.setFont(QFont("Segoe UI Variable", 16))
        user_label.setAlignment(Qt.AlignCenter)

        # Timer Display
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setFont(QFont("Segoe UI Variable", 24))
        self.timer_label.setAlignment(Qt.AlignCenter)

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setFont(QFont("Segoe UI Variable", 12))
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        logout_button.clicked.connect(self.logout_handler)

        # Add to Layout
        layout.addWidget(user_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        layout.addWidget(logout_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.start_timer()

    def start_timer(self):
        """Start the timer."""
        self.start_time = QTime(0, 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        """Update the timer text."""
        self.start_time = self.start_time.addSecs(1)
        self.timer_label.setText(self.start_time.toString("HH:mm:ss"))

    def logout_handler(self):
        """Handle logout and return to check-in screen."""
        if self.timer:
            self.timer.stop()
        self.init_checkin_ui()

    def shutdown_handler(self):
        """Shutdown the computer (Windows only)."""
        os.system("shutdown /s /t 1")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckInSystem()
    app.exec_()
