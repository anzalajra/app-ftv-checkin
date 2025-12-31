import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt


class CheckInSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.start_time = None  # Timer start time
        self.timer = None       # QTimer instance
        self.user_name = None   # Name of the user who checked in
        self.init_checkin_ui()  # Set up fullscreen check-in page first

    def clear_layout(self):
        """Remove the current layout (if any) to prevent overlap."""
        if self.layout() is not None:
            # Create a temporary widget to clear the layout
            QWidget().setLayout(self.layout())

    def init_checkin_ui(self):
        """Initialize the fullscreen check-in UI."""
        self.clear_layout()  # Clear the current layout first
        self.setWindowTitle("Film dan Televisi Check-In")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window border
        self.showFullScreen()  # Set Fullscreen for check-in page

        # Main Layout for Check-In
        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(50, 50, 50, 50)  # Tambahkan margin di setiap sisi
        layout_main.setSpacing(20)  # Spasi antar elemen

        # Title Label
        self.label_title = QLabel("Selamat Datang! Silakan Check-In")
        self.label_title.setFont(QFont("Segoe UI Variable", 24))
        self.label_title.setStyleSheet("color: #000000; font-weight: bold;")  # Warna teks dan ketebalan
        self.label_title.setAlignment(Qt.AlignCenter)
        layout_main.addWidget(self.label_title)

        # Form Input
        form_layout = QVBoxLayout()
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nama")
        self.name_input.setStyleSheet("""
            background-color: #FFFFFF;  /* Warna putih */
            font-size: 16px;
            padding: 8px;
            border: 2px solid #CCCCCC;
            border-radius: 10px;  /* Rounded Corner */
        """)
        self.name_input.setFont(QFont("Segoe UI Variable", 14))
        self.name_input.setAlignment(Qt.AlignCenter)

        self.nim_input = QLineEdit(self)
        self.nim_input.setPlaceholderText("NIM")
        self.nim_input.setStyleSheet("""
            background-color: #FFFFFF;
            font-size: 16px;
            padding: 8px;
            border: 2px solid #CCCCCC;
            border-radius: 10px;
        """)
        self.nim_input.setFont(QFont("Segoe UI Variable", 14))
        self.nim_input.setAlignment(Qt.AlignCenter)

        submit_button = QPushButton("Check-In", self)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;  /* Biru ala Windows */
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 12px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #005A9E;  /* Biru lebih gelap saat hover */
            }
        """)
        submit_button.setFont(QFont("Arial", 14))
        submit_button.clicked.connect(self.handle_checkin)

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.nim_input)
        form_layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        layout_main.addLayout(form_layout)

        # Shutdown Button at Bottom Right
        button_layout = QHBoxLayout()
        shutdown_button = QPushButton("Shutdown")
        shutdown_button.setFont(QFont("Arial", 10))
        shutdown_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;  /* Tombol shutdown warna merah */
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #B20000;  /* Warna merah lebih gelap saat hover */
            }
        """)
        shutdown_button.clicked.connect(self.shutdown_handler)

        button_layout.addStretch()
        button_layout.addWidget(shutdown_button)
        layout_main.addLayout(button_layout)

        # Set the layout
        self.setLayout(layout_main)

    def handle_checkin(self):
        """Handle the check-in process."""
        name = self.name_input.text().strip()
        nim = self.nim_input.text().strip()

        if not name or not nim:
            self.label_title.setText("Nama dan NIM harus diisi!")
            self.label_title.setStyleSheet("color: red;")
            return

        # Store the user's name and proceed to timer
        self.user_name = name
        self.label_title.setStyleSheet("color: black;")
        self.close()  # Close fullscreen check-in page
        self.init_timer_ui()  # Open the Timer Page

    def init_timer_ui(self):
        """Initialize the Timer UI (minimizable, draggable, and no close button)."""
        self.clear_layout()
        self.setWindowTitle("Timer Aktif")
        self.setGeometry(100, 100, 300, 200)
        # Disable close button and make it always on top
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.Tool)
    
        # Layout
        layout = QVBoxLayout()
    
        # User name label
        self.user_label = QLabel(f"Hi, {self.user_name}")
        self.user_label.setFont(QFont("Segoe UI Variable", 16))
        self.user_label.setAlignment(Qt.AlignCenter)
    
        # Timer label
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setFont(QFont("Segoe UI Variable", 24))
        self.timer_label.setAlignment(Qt.AlignCenter)
    
        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setFont(QFont("Segoe UI Variable", 12))
        self.logout_button.setStyleSheet("""
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
        self.logout_button.clicked.connect(self.logout_handler)
    
        # Add to layout
        layout.addWidget(self.user_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.show()
    
        # Initialize drag variables
        self._is_dragging = False  # To track dragging status
        self._drag_start_pos = None  # Initial dragging position

        # Start the timer
        self.start_time = QTime.currentTime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every 1 second

        self.show()  # Show timer page
    def closeEvent(self, event):
        """Override the close event to prevent the window from being closed."""
        event.ignore()  # Ignore the close event, so the window won't close
    
    def mousePressEvent(self, event):
        """Initialize dragging when the mouse is pressed."""
        if event.button() == Qt.LeftButton:  # Only left-click is used for dragging
            self._is_dragging = True
            self._drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle window moving during drag."""
        if self._is_dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_start_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Stop dragging when the mouse is released."""
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            event.accept()
        
    def update_timer(self):
        """Update the timer label."""
        elapsed = self.start_time.secsTo(QTime.currentTime())
        elapsed_text = QTime(0, 0).addSecs(elapsed).toString("HH:mm:ss")
        self.timer_label.setText(elapsed_text)

    def logout_handler(self):
        """Handle logout button."""
        self.timer.stop()  # Stop the timer
        self.close()  # Close the timer page
        self.start_time = None  # Reset timer
        self.user_name = None  # Reset user name
        self.init_checkin_ui()  # Reopen the fullscreen check-in page

    def shutdown_handler(self):
        """Shutdown the computer (for Windows 11)."""
        print("Shutdown initiated.")  # Optional log for testing
        os.system("shutdown /s /t 1")  # Shutdown computer immediately


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckInSystem()
    sys.exit(app.exec_())
