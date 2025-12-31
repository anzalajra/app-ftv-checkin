import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QTime


class CheckInSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window properties
        self.setWindowTitle("Film dan Televisi User Check-In")
        # Set to fullscreen and always on top to prevent access to other apps
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            border-radius: 20px;
            background-image: url('wallpaper_ftv.jpg');
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        """)  # Admin dapat mengganti 'wallpaper_ftv.jpg' dengan gambar lain sesuai kebutuhan

        # Layouts
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Header: Title
        title = QLabel("Film dan Televisi User Check-In")
        title.setFont(QFont("Segoe UI Variable", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Masukkan Nama")
        self.name_input.setFont(QFont("Segoe UI Variable", 10))

        self.nim_input = QLineEdit()
        self.nim_input.setPlaceholderText("Masukkan NIM")
        self.nim_input.setFont(QFont("Segoe UI Variable", 10))

        # Buttons
        submit_btn = QPushButton("Check-In")
        submit_btn.setFont(QFont("Segoe UI Variable", 10))
        submit_btn.setStyleSheet(self.button_style())
        submit_btn.clicked.connect(self.submit_handler)

        shutdown_btn = QPushButton("Shutdown")
        shutdown_btn.setFont(QFont("Segoe UI Variable", 10))
        shutdown_btn.setStyleSheet(self.button_style())
        shutdown_btn.clicked.connect(self.shutdown_handler)

        sleep_btn = QPushButton("Sleep")
        sleep_btn.setFont(QFont("Segoe UI Variable", 10))
        sleep_btn.setStyleSheet(self.button_style())
        sleep_btn.clicked.connect(self.sleep_handler)

        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(shutdown_btn)
        button_layout.addWidget(sleep_btn)

        # Footer: Copyright
        copyright_label = QLabel("© 2026 Divisi IT FTV UPI")
        copyright_label.setFont(QFont("Segoe UI Variable", 8))
        copyright_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.nim_input)
        layout.addLayout(button_layout)
        layout.addWidget(copyright_label)

        self.setLayout(layout)

    def button_style(self):
        return """
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """

    def submit_handler(self):
        name = self.name_input.text()
        nim = self.nim_input.text()

        if not name or not nim:
            self.show_message("Error", "Harap masukkan Nama dan NIM.")
            return

        self.hide()
        self.monitor_window = PipWindow(name)
        self.monitor_window.showFullScreen()  # Show in fullscreen mode

    def shutdown_handler(self):
        sys.exit()  # Simulate shutdown for now

    def sleep_handler(self):
        print("Sleep triggered!")  # Replace with actual sleep command

    def show_message(self, title, message):
        msg = QLabel(message)
        msg.setWindowTitle(title)
        msg.setStyleSheet("font-size: 12px; padding: 10px;")
        msg.show()


class PipWindow(QWidget):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.start_time = QTime.currentTime()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Monitoring: {self.user_name}")
        # Set to fullscreen and always on top to prevent access to other apps
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #f8f8f8; border-radius: 15px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        user_label = QLabel(f"User: {self.user_name}")
        user_label.setFont(QFont("Segoe UI Variable", 12))
        user_label.setAlignment(Qt.AlignCenter)

        self.timer_label = QLabel("Durasi Aktif: 00:00:00")
        self.timer_label.setFont(QFont("Segoe UI Variable", 10))
        self.timer_label.setAlignment(Qt.AlignCenter)

        logout_btn = QPushButton("Logout")
        logout_btn.setFont(QFont("Segoe UI Variable", 10))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        logout_btn.clicked.connect(self.logout_handler)

        layout.addWidget(user_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(logout_btn)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.setLayout(layout)

    def update_timer(self):
        # Calculate elapsed seconds correctly
        elapsed = self.start_time.secsTo(QTime.currentTime())
        # Ensure elapsed time is non-negative (handles system time changes)
        if elapsed < 0:
            elapsed = 0
        elapsed_text = QTime(0, 0).addSecs(elapsed).toString("hh:mm:ss")
        self.timer_label.setText(f"Durasi Aktif: {elapsed_text}")

    def logout_handler(self):
        self.close()
        self.checkin_window = CheckInSystem()
        self.checkin_window.showFullScreen()  # Show in fullscreen mode


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckInSystem()
    window.showFullScreen()  # Show in fullscreen mode
    sys.exit(app.exec_())
