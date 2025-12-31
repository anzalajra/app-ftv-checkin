import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QTime

class CheckInSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Fullscreen
        self.setWindowTitle("Film and Televisi Check-In")
        self.setGeometry(600, 200, 400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Layout
        layout = QVBoxLayout()
        self.timer_label = QLabel("Durasi Aktif: 00:00:00")
        self.timer_label.setFont(QFont("Segoe UI", 14))
        self.timer_label.setAlignment(Qt.AlignCenter)

        logout_btn = QPushButton("Logout")
        logout_btn.setFont(QFont("Segoe UI", 12))
        logout_btn.clicked.connect(self.logout_handler)

        layout.addWidget(self.timer_label)
        layout.addWidget(logout_btn)
        self.setLayout(layout)

        # Timer logic
        self.start_time = QTime.currentTime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update setiap 1 detik

    def update_timer(self):
        elapsed = QTime(0, 0).secsTo(self.start_time.secsTo(QTime.currentTime()))
        elapsed_text = QTime(0, 0).addSecs(elapsed).toString("hh:mm:ss")
        self.timer_label.setText(f"Durasi Aktif: {elapsed_text}")

    def logout_handler(self):
        self.timer.stop()
        self.close()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = CheckInSystem()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: {e}")
