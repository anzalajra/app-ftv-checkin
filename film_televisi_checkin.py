import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QInputDialog
import ctypes
from ctypes import wintypes
import threading
import time

# GANTI SELURUH bagian KEYBOARD BLOCKER dengan ini: 

# ============ KEYBOARD BLOCKER ============
class KBDLLHOOKSTRUCT(ctypes.Structure):
    """Structure for low-level keyboard input event."""
    _fields_ = [
        ("vkCode", ctypes.c_ulong),
        ("scanCode", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

# Load user32.dll explicitly
user32 = ctypes.windll.user32

# Define function prototypes
user32.SetWindowsHookExW.argtypes = [
    ctypes.c_int,
    ctypes.c_void_p,
    ctypes.wintypes.HMODULE,
    ctypes.wintypes.DWORD
]
user32.SetWindowsHookExW.restype = ctypes.c_void_p

user32.CallNextHookEx.argtypes = [
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM
]
user32.CallNextHookEx.restype = ctypes.c_long

user32.UnhookWindowsHookEx.argtypes = [ctypes.c_void_p]
user32.UnhookWindowsHookEx.restype = ctypes.wintypes.BOOL

user32.GetMessageW.argtypes = [
    ctypes.POINTER(ctypes.wintypes.MSG),
    ctypes.wintypes.HWND,
    ctypes.c_uint,
    ctypes.c_uint
]
user32.GetMessageW.restype = ctypes.wintypes.BOOL

# Callback type for low-level keyboard hook
LowLevelKeyboardProc = ctypes.CFUNCTYPE(
    ctypes.c_long,
    ctypes.c_int,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM
)

class KeyboardBlocker: 
    """Block system keyboard shortcuts like Alt+Tab, Win key, etc."""
    
    WH_KEYBOARD_LL = 13
    
    # Keys to block
    VK_LWIN = 0x5B
    VK_RWIN = 0x5C
    VK_TAB = 0x09
    VK_ESCAPE = 0x1B
    VK_DELETE = 0x2E
    VK_F4 = 0x73
    VK_LALT = 0xA4
    VK_RALT = 0xA5
    VK_LCONTROL = 0xA2
    VK_RCONTROL = 0xA3
    
    def __init__(self):
        self.hooked = None
        self.block_enabled = False
        self._hook_thread = None
        self._running = False
        # Keep reference to callback to prevent garbage collection
        self._callback = LowLevelKeyboardProc(self._keyboard_proc)
    
    def _keyboard_proc(self, nCode, wParam, lParam):
        """Low-level keyboard hook callback."""
        if nCode >= 0 and self.block_enabled:
            kbd = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk_code = kbd.vkCode
            
            # Block Windows keys
            if vk_code in (self.VK_LWIN, self.VK_RWIN):
                return 1
            
            # Check modifier states
            alt_pressed = (user32.GetAsyncKeyState(self.VK_LALT) & 0x8000 or 
                          user32.GetAsyncKeyState(self.VK_RALT) & 0x8000)
            ctrl_pressed = (user32.GetAsyncKeyState(self.VK_LCONTROL) & 0x8000 or
                           user32.GetAsyncKeyState(self.VK_RCONTROL) & 0x8000)
            
            # Block Alt combinations
            if alt_pressed and vk_code in (self.VK_TAB, self.VK_ESCAPE, self.VK_F4):
                return 1
            
            # Block Ctrl combinations
            if ctrl_pressed and vk_code in (self.VK_TAB, self.VK_ESCAPE):
                return 1
        
        return user32.CallNextHookEx(self.hooked, nCode, wParam, lParam)
    
    def _hook_thread_func(self):
        """Thread function to run the message loop."""
        # Use 0 for hMod to work with Python threads
        self.hooked = user32.SetWindowsHookExW(
            self.WH_KEYBOARD_LL,
            self._callback,
            0,  # Use 0 instead of GetModuleHandleW(None)
            0
        )
        
        if not self.hooked:
            error = ctypes.windll.kernel32.GetLastError()
            print(f"Failed to install keyboard hook!  Error code: {error}")
            return
        
        print("Keyboard hook installed successfully!")
        
        # Message loop
        msg = ctypes.wintypes.MSG()
        while self._running:
            bRet = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if bRet == 0 or bRet == -1:
                break
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
        
        # Cleanup
        if self.hooked:
            user32.UnhookWindowsHookEx(self.hooked)
            self.hooked = None
            print("Keyboard hook uninstalled.")
    
    def install_hook(self):
        """Install the keyboard hook in a separate thread."""
        if self._hook_thread is None or not self._hook_thread.is_alive():
            self._running = True
            self._hook_thread = threading.Thread(target=self._hook_thread_func, daemon=True)
            self._hook_thread.start()
            time.sleep(0.2)
    
    def enable_blocking(self):
        """Enable keyboard blocking."""
        self.block_enabled = True
        print("Keyboard blocking ENABLED")
        
    def disable_blocking(self):
        """Disable keyboard blocking."""
        self.block_enabled = False
        print("Keyboard blocking DISABLED")
        
    def uninstall_hook(self):
        """Remove the keyboard hook."""
        self._running = False
        # Post quit message to break GetMessageW loop
        if self._hook_thread and self._hook_thread.is_alive():
            user32.PostThreadMessageW(self._hook_thread.ident, 0x0012, 0, 0)  # WM_QUIT
            self._hook_thread.join(timeout=2.0)
        self.hooked = None

# Global keyboard blocker instance
keyboard_blocker = KeyboardBlocker()
# ============ END KEYBOARD BLOCKER ============

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

    def disable_taskbar(self):
        """Hide and disable the Windows taskbar."""
        try:
            # Find and hide main taskbar
            taskbar = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar:
                ctypes.windll.user32.ShowWindow(taskbar, 0)  # SW_HIDE = 0
            
            # Find and hide secondary taskbar (for multi-monitor)
            secondary = ctypes.windll.user32.FindWindowW("Shell_SecondaryTrayWnd", None)
            if secondary:
                ctypes.windll.user32.ShowWindow(secondary, 0)
                
            print("Taskbar HIDDEN")
        except Exception as e:
            print(f"Error hiding taskbar: {e}")
    
    def enable_taskbar(self):
        """Show and enable the Windows taskbar."""
        try:
            # Find and show main taskbar
            taskbar = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar: 
                ctypes.windll.user32.ShowWindow(taskbar, 9)  # SW_RESTORE = 9
            
            # Find and show secondary taskbar (for multi-monitor)
            secondary = ctypes.windll.user32.FindWindowW("Shell_SecondaryTrayWnd", None)
            if secondary: 
                ctypes.windll.user32.ShowWindow(secondary, 9)
                
            print("Taskbar SHOWN")
        except Exception as e:
            print(f"Error showing taskbar: {e}")

    def init_checkin_ui(self):
        """Initialize the fullscreen check-in UI."""
        self.clear_layout()  # Clear the current layout first
        self.setWindowTitle("Film dan Televisi Check-In")

        # PENTING: Hide dulu, set flags, baru show
        self.hide()
        
        # Set window flags untuk fullscreen tanpa frame
        self.setWindowFlags(Qt. Window | Qt. FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # Set geometry ke screen size
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        # Show window
        self.show()
        self.showFullScreen()
        
        # Force update dan activate
        self.activateWindow()
        self.raise_()
        QApplication.processEvents()

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
        
        # Enable Enter key to submit - pindah focus atau submit
        self.name_input.returnPressed.connect(self._on_name_enter)
        self.nim_input.returnPressed.connect(self._on_nim_enter)

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

        # Admin Close Button (hidden by default, show with Ctrl+A)
        self.admin_close_button = QPushButton("Admin Close")
        self.admin_close_button.setFont(QFont("Arial", 12))
        self.admin_close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color:  white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color:  darkred;
            }
        """)
        self.admin_close_button.clicked.connect(self.admin_close_dialog)
        self.admin_close_button.hide()  # Hidden by default
        layout_main.addWidget(self.admin_close_button, alignment=Qt.AlignCenter)

        # Set the layout
        self.setLayout(layout_main)
        self.show()  # Pastikan ini dipanggil
        # Disable keyboard blocking for timer page (user can use computer)
        keyboard_blocker.enable_blocking()
        
        # Re-enable taskbar when timer is active
        self.disable_taskbar()

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

    def _on_name_enter(self):
        """Handle Enter key on name input - move focus to NIM input."""
        self.nim_input.setFocus()
    
    def _on_nim_enter(self):
        """Handle Enter key on NIM input - trigger check-in."""
        # Gunakan QTimer untuk delay sedikit agar tidak konflik
        QTimer.singleShot(100, self.handle_checkin)

    def init_timer_ui(self):
        """Initialize the Timer UI (minimizable, draggable, and resizable)."""
        self.clear_layout()
        self.setWindowTitle("Timer Aktif")
        self.setGeometry(100, 100, 300, 200)
        
        # Frameless tapi bisa resize
        self.setWindowFlags(Qt. FramelessWindowHint | Qt.Tool)
        
        # Set minimum size
        self.setMinimumSize(200, 150)
        
        # Enable mouse tracking untuk resize
        self.setMouseTracking(True)
        
        # Resize margin (area di pinggir untuk resize)
        self._resize_margin = 10
        self._resizing = False
        self._resize_direction = None
    
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

        # Admin Close
        self.admin_close_button = QPushButton("Admin Close")
        self.admin_close_button.setFont(QFont("Arial", 12))  # Atur gaya font
        self.admin_close_button.setStyleSheet("""
            QPushButton {
                background-color: red;  /* Tombol merah untuk admin */
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.admin_close_button.clicked.connect(self.admin_close_dialog)  # Buatkan fungsi untuk tombol nanti
        self.admin_close_button.hide()  # Sembunyikan tombol secara default
        layout.addWidget(self.admin_close_button, alignment=Qt.AlignCenter)  # Masukkan tombol dalam layout

        # Tambahkan dalam init_timer_ui di koneksi tombol
        self.admin_close_button.clicked.connect(self.admin_close_dialog)
    
        # Add to layout
        layout.addWidget(self.user_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)
    
        # Initialize drag variables
        self._is_dragging = False  # To track dragging status
        self._drag_start_pos = None  # Initial dragging position

        # Start the timer
        self.start_time = QTime.currentTime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every 1 second
        
        self.setLayout(layout)
        self.show()  # Show timer page
        
        keyboard_blocker.disable_blocking() # Enable keyboard blocking during fullscreen check-in
        self.enable_taskbar() # Disable taskbar during check-in

    def keyPressEvent(self, event):
        """Detect specific key combinations for Admin functionalities."""
        # Jika Ctrl + A ditekan, tampilkan Admin Close button
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_A:
            if hasattr(self, 'admin_close_button') and self.admin_close_button: 
                try:
                    self.admin_close_button.show()
                except RuntimeError: 
                    pass  # Button sudah dihapus, ignore
        # Jika Esc ditekan, sembunyikan Admin Close button
        elif event.key() == Qt.Key_Escape: 
            if hasattr(self, 'admin_close_button') and self.admin_close_button: 
                try: 
                    self.admin_close_button.hide()
                except RuntimeError:
                    pass  # Button sudah dihapus, ignore

    def admin_close_dialog(self):
        """Display a dialog for Admin PIN verification before closing the app."""
        pin, ok = QInputDialog.getText(self, "Admin Authentication", "Masukkan PIN Admin:", QLineEdit.Password)
        if ok and pin == "9999": # GANTI DENGAN PIN YANG DIINGINKAN
            # Cleanup sebelum quit
            keyboard_blocker.disable_blocking()
            keyboard_blocker.uninstall_hook()
            self.enable_taskbar()
            
            # Stop timer jika ada
            if self.timer and self.timer.isActive():
                self.timer.stop()
            
            # Quit aplikasi
            QApplication.quit()
        elif ok:
            print("PIN Salah!")

    
    def closeEvent(self, event):
        """Override the close event to prevent the window from being closed."""
        event.ignore()  # Ignore the close event, so the window won't close
    
    def mousePressEvent(self, event):
        """Initialize dragging or resizing when the mouse is pressed."""
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            rect = self.rect()
            
            # Cek apakah di area resize (pinggir window)
            self._resize_direction = self._get_resize_direction(pos, rect)
            
            if self._resize_direction:
                self._resizing = True
                self._resize_start_pos = event.globalPos()
                self._resize_start_geometry = self.geometry()
            else:
                # Dragging
                self._is_dragging = True
                self._drag_start_pos = event.globalPos() - self. frameGeometry().topLeft()
            
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle window moving or resizing during drag."""
        if self._resizing and event.buttons() == Qt.LeftButton:
            self._do_resize(event. globalPos())
            event.accept()
        elif self._is_dragging and event.buttons() == Qt.LeftButton:
            self. move(event.globalPos() - self._drag_start_pos)
            event.accept()
        else:
            # Update cursor berdasarkan posisi
            self._update_cursor(event.pos())
    
    def mouseReleaseEvent(self, event):
        """Stop dragging or resizing when the mouse is released."""
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            self._resizing = False
            self._resize_direction = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        
    def update_timer(self):
        """Update the timer label."""
        elapsed = self.start_time.secsTo(QTime.currentTime())
        elapsed_text = QTime(0, 0).addSecs(elapsed).toString("HH:mm:ss")
        self.timer_label.setText(elapsed_text)

    def logout_handler(self):
        """Handle logout button."""
        self.timer.stop()  # Stop the timer
        self.start_time = None  # Reset timer
        self.user_name = None  # Reset user name
        
        # Hide window dulu sebelum reinitialize
        self.hide()
        
        # Re-enable keyboard blocking for check-in page
        keyboard_blocker.enable_blocking()
        self.disable_taskbar()
        
        # Gunakan QTimer untuk delay agar window state ter-reset dengan benar
        QTimer.singleShot(100, self._reinit_checkin)
    
    def _reinit_checkin(self):
        """Reinitialize check-in UI after logout."""
        # Destroy current window state completely
        self.hide()
        
        # Clear window flags dulu
        self.setWindowFlags(Qt.Widget)
        
        # Kemudian panggil init
        self.init_checkin_ui()

    def _get_resize_direction(self, pos, rect):
        """Determine resize direction based on mouse position."""
        margin = self._resize_margin if hasattr(self, '_resize_margin') else 10
        
        left = pos.x() < margin
        right = pos.x() > rect.width() - margin
        top = pos.y() < margin
        bottom = pos.y() > rect.height() - margin
        
        if top and left:
            return 'top-left'
        elif top and right: 
            return 'top-right'
        elif bottom and left:
            return 'bottom-left'
        elif bottom and right:
            return 'bottom-right'
        elif left: 
            return 'left'
        elif right:
            return 'right'
        elif top:
            return 'top'
        elif bottom: 
            return 'bottom'
        return None
    
    def _update_cursor(self, pos):
        """Update cursor based on position for resize indication."""
        if not hasattr(self, '_resize_margin'):
            return
            
        direction = self._get_resize_direction(pos, self.rect())
        
        if direction in ('left', 'right'):
            self.setCursor(Qt.SizeHorCursor)
        elif direction in ('top', 'bottom'):
            self.setCursor(Qt.SizeVerCursor)
        elif direction in ('top-left', 'bottom-right'):
            self.setCursor(Qt. SizeFDiagCursor)
        elif direction in ('top-right', 'bottom-left'):
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
    
    def _do_resize(self, global_pos):
        """Perform the resize operation."""
        if not self._resize_direction:
            return
            
        diff = global_pos - self._resize_start_pos
        geo = self._resize_start_geometry
        
        min_width = self.minimumWidth()
        min_height = self.minimumHeight()
        
        new_geo = self.geometry()
        
        if 'right' in self._resize_direction:
            new_width = max(min_width, geo. width() + diff.x())
            new_geo.setWidth(new_width)
        if 'bottom' in self._resize_direction:
            new_height = max(min_height, geo.height() + diff.y())
            new_geo. setHeight(new_height)
        if 'left' in self._resize_direction:
            new_width = max(min_width, geo.width() - diff.x())
            if new_width > min_width:
                new_geo.setLeft(geo.left() + diff.x())
        if 'top' in self._resize_direction:
            new_height = max(min_height, geo.height() - diff.y())
            if new_height > min_height:
                new_geo.setTop(geo.top() + diff.y())
        
        self.setGeometry(new_geo)

    def shutdown_handler(self):
        """Shutdown the computer (for Windows 11)."""
        print("Shutdown initiated.")  # Optional log for testing
        os.system("shutdown /s /t 1")  # Shutdown computer immediately


if __name__ == "__main__":
    # Install keyboard hook
    keyboard_blocker.install_hook()
    
    app = QApplication(sys.argv)
    window = CheckInSystem()
    
    result = app.exec_()
    
    # Cleanup:  uninstall hook and restore taskbar
    keyboard_blocker.uninstall_hook()
    window.enable_taskbar()
    
    sys.exit(result)
