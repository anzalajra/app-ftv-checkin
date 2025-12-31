import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt


class CheckInSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.start_time = None  # Timer start time
        self.timer = None       # QTimer instance
        self.init_checkin_ui()  # Set up full-screen check-in page first

    def init_checkin_ui(self):
        """Initialize the fullscreen check-in UI."""
        self.setWindowTitle("Film dan Televisi Check-In")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window border
        self.showFullScreen()  # Set Fullscreen for check-in page

        layout = QVBoxLayout()

        self.label_title = QLabel("Silakan Check-In Untuk Melanjutkan")
        self.label_title.setFont(QFont("Arial", 16))
        self.label_title.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nama")
        self.name_input.setFont(QFont("Arial", 12))

        self.nim_input = QLineEdit(self)
        self.nim_input.setPlaceholderText("NIM")
        self.nim_input.setFont(QFont("Arial", 12))

        self.submit_button = QPushButton("Check-In", self)
        self.submit_button.setFont(QFont("Arial", 12))
        self.submit_button.clicked.connect(self.handle_checkin)

        layout.addWidget(self.label_title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.nim_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def handle_checkin(self):
        """Handle the check-in process."""
        name = self.name_input.text().strip()
        nim = self.nim_input.text().strip()

        if not name or not nim:
            # If no input, show error message
            self.label_title.setText("Nama dan NIM harus diisi!")
            self.label_title.setStyleSheet("color: red;")
            return

        # Check-in successful, proceed to timer window
        self.label_title.setStyleSheet("color: black;")
        self.label_title.setText("Check-In berhasil, memulai aplikasi...")
        self.close()  # Close fullscreen check-in page
        self.init_timer_ui()  # Open the Timer Page

    def init_timer_ui(self):
        """Initialize the timer page (not fullscreen)."""
        self.setWindowTitle("Film dan Televisi - Timer")
        self.setGeometry(400, 200, 400, 200)

        layout = QVBoxLayout()

        self.timer_label = QLabel("Durasi Aktif: 00:00:00")
        self.timer_label.setFont(QFont("Arial", 16))
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setFont(QFont("Arial", 12))
        self.logout_button.clicked.connect(self.logout_handler)

        layout.addWidget(self.timer_label)
        layout.addWidget(self.logout_button)
        self.setLayout(layout)

        # Start the timer
        self.start_time = QTime.currentTime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every 1 second

        self.show()  # Show timer page

    def update_timer(self):
        """Update the timer label."""
        elapsed = QTime(0, 0).secsTo(self.start_time.secsTo(QTime.currentTime()))
        elapsed_text = QTime(0, 0).addSecs(elapsed).toString("hh:mm:ss")
        self.timer_label.setText(f"Durasi Aktif: {elapsed_text}")

    def logout_handler(self):
        """Handle logout function."""
        self.timer.stop()  # Stop the timer
        self.close()  # Exit the application


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckInSystem()
    window.show()
    sys.exit(app.exec_())
