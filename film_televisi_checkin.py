import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt


class CheckInSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.start_time = None  # Timer start time
        self.timer = None       # QTimer instance
        self.init_checkin_ui()  # Set up fullscreen check-in page first

    def init_checkin_ui(self):
        """Initialize the fullscreen check-in UI."""
        self.setWindowTitle("Film dan Televisi Check-In")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window border
        self.showFullScreen()  # Set Fullscreen for check-in page

        layout_main = QVBoxLayout()

        # Title Label
        self.label_title = QLabel("Selamat Datang! Silakan Check-In")
        self.label_title.setFont(QFont("Arial", 18))
        self.label_title.setAlignment(Qt.AlignCenter)
        layout_main.addWidget(self.label_title)

        # Form Input
        form_layout = QVBoxLayout()
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nama")
        self.name_input.setFont(QFont("Arial", 14))
        self.name_input.setAlignment(Qt.AlignCenter)

        self.nim_input = QLineEdit(self)
        self.nim_input.setPlaceholderText("NIM")
        self.nim_input.setFont(QFont("Arial", 14))
        self.nim_input.setAlignment(Qt.AlignCenter)

        submit_button = QPushButton("Check-In", self)
        submit_button.setFont(QFont("Arial", 14))
        submit_button.clicked.connect(self.handle_checkin)

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.nim_input)
        form_layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        layout_main.addLayout(form_layout)

        # Shutdown and Sleep Buttons at Bottom Right
        button_layout = QHBoxLayout()
        shutdown_button = QPushButton("Shutdown")
        shutdown_button.setFont(QFont("Arial", 10))
        shutdown_button.setStyleSheet("background-color: #cc0000; color: white; padding: 5px;")
        shutdown_button.clicked.connect(self.shutdown_handler)

        sleep_button = QPushButton("Sleep")
        sleep_button.setFont(QFont("Arial", 10))
        sleep_button.setStyleSheet("background-color: #008080; color: white; padding: 5px;")
        sleep_button.clicked.connect(self.sleep_handler)

        button_layout.addStretch()
        button_layout.addWidget(shutdown_button)
        button_layout.addWidget(sleep_button)

        layout_main.addLayout(button_layout)

        self.setLayout(layout_main)

    def handle_checkin(self):
        """Handle the check-in process."""
        name = self.name_input.text().strip()
        nim = self.nim_input.text().strip()

        if not name or not nim:
            self.label_title.setText("Nama dan NIM harus diisi!")
            self.label_title.setStyleSheet("color: red;")
            return

        # Check-in successful, proceed to timer window
        self.label_title.setStyleSheet("color: black;")
        self.label_title.setText("Check-In berhasil, memulai aplikasi...")
        self.close()  # Close fullscreen check-in page
        self.init_timer_ui()  # Open the Timer Page

    def init_timer_ui(self):
        """Initialize the timer page (minimizable and draggable)."""
        self.setWindowTitle("Film dan Televisi - Timer")
        self.setGeometry(400, 200, 400, 200)
        self.setWindowFlags(Qt.Tool)  # Makes the application run without taskbar icon

        layout = QVBoxLayout()

        self.timer_label = QLabel("Durasi Aktif: 00:00:00")
        self.timer_label.setFont(QFont("Arial", 16))
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setFont(QFont("Arial", 12))
        self.logout_button.clicked.connect(self.logout_handler)

        layout.addWidget(self.timer_label)
        layout.addWidget(self.logout_button, alignment=Qt.AlignHCenter)
        self.setLayout(layout)

        # Start the timer
        self.start_time = QTime.currentTime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every 1 second

        self.show()  # Show timer page

    def update_timer(self):
        """Update the timer label."""
        elapsed = self.start_time.secsTo(QTime.currentTime())
        elapsed_text = QTime(0, 0).addSecs(elapsed).toString("hh:mm:ss")
        self.timer_label.setText(f"Durasi Aktif: {elapsed_text}")

    def logout_handler(self):
        """Handle logout button."""
        self.timer.stop()  # Stop the timer
        self.close()  # Close the timer page
        self.init_checkin_ui()  # Reopen the fullscreen check-in page

    def shutdown_handler(self):
        """Simulate shutdown."""
        print("Shutdown button clicked")  # Replace with actual shutdown logic if necessary

    def sleep_handler(self):
        """Simulate sleep."""
        print("Sleep button clicked")  # Replace with actual sleep logic if necessary


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckInSystem()
    sys.exit(app.exec_())
