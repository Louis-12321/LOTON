# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________
from PySide6.QtWidgets import (
    QApplication, QLineEdit, QMessageBox, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QPushButton, QSizePolicy
)
from path import asset_path
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
import Login_screen_userpass
import sys
import random


class Login(QWidget):
    def __init__(self):
        super().__init__()

        self._loginTimer = random.randint(1200, 2000)

        self._spinner_frames = ["|", "/", "-", "\\"]
        self._spinner_index = 0
        self._pending_action = None
        self._authenticated_user = None

        # Window setup
        self.setWindowTitle("LOTON Login")
        self.resize(1920, 1080)
        self.setMinimumSize(1080, 720)

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)

        # Root container
        self.root = QWidget(self)
        self.root.setStyleSheet("""
            QWidget {
                background-color: #003eff;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.root)

        root_layout = QVBoxLayout(self.root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        # Title bar
        self.title_bar = QWidget(self.root)
        self.title_bar.setFixedHeight(36)
        self.title_bar.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.title_bar.setStyleSheet("""
            background-color: #002bbd;
        """)

        title_layout = QGridLayout(self.title_bar)  
        title_layout.setContentsMargins(8, 0, 8, 0)

        title = QLabel("LOTON Login Menu")
        title.setStyleSheet("color: white; font-size: 18px;")

        btn_min = QPushButton("-")
        btn_close = QPushButton("x")

        for btn in (btn_min, btn_close):
            btn.setFixedSize(28, 24)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0040ff;
                    color: white;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #ff4444;
                }
            """)
            btn.setFocusPolicy(Qt.NoFocus)

        btn_min.clicked.connect(self.showMinimized)
        btn_close.clicked.connect(self.close)

        title_layout.addWidget(title, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        title_layout.addWidget(btn_min, 0, 1)
        title_layout.setColumnStretch(0, 1)
        title_layout.addWidget(btn_close, 0, 2)
        root_layout.addWidget(self.title_bar)

        self.content = QWidget(self.root)
        root_layout.addWidget(self.content)

        #==========================
        #    BORDER
        #==========================
        #Ignore the that the thing is named "background" instead of border
        self.background = QLabel(self.content) #A rectangle that will serve as the border for the login screen
        self.background.setGeometry(510, 250, 850, 620)
        self.background.setStyleSheet("""
            border: 3px solid white;
            border-radius: 16px;
        """)
        self.background.setAlignment(Qt.AlignCenter)


        #==========================
        #       LOTON LOGO
        #==========================
        self.lotonlogo = QLabel(self.content)
        up_path = asset_path("Real assets", "LOTON text.png")
        self.lotonlogo.setPixmap(QPixmap(up_path))
        self.lotonlogo.setGeometry(662, 300, 595, 121)
        self.lotonlogo.setScaledContents(True)

        #==========================
        #     WELCOME MESSAGE
        #==========================
        self.welcomemessage = QLabel("The OS made in Python", self.content)
        self.welcomemessage.setAlignment(Qt.AlignCenter)
        self.welcomemessage.setGeometry(760, 435, 350, 30)
        self.welcomemessage.setStyleSheet("color: white; font-size: 30px;font-weight: bold;font-family: Bahnschrift;")

        #==========================
        #USERNAME + PASSWORD FIELDS
        #==========================
        self.username_field = QLineEdit(self.content)
        self.username_field.setGeometry(720, 500, 430, 60)
        self.username_field.setPlaceholderText("Username")
        self.username_field.setText("ADMIN")
        self.username_field.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                font-size: 18px;
                border-radius: 8px;
                padding: 8px;
            }
        """)

        self.password_field = QLineEdit(self.content)
        self.password_field.setGeometry(720, 580, 430, 60)
        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setText("123456789")
        self.password_field.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                font-size: 18px;
                border-radius: 8px;
                padding: 8px;
            }
        """)

        self.loginbutton = QPushButton("Login", self.content)
        self.loginbutton.setGeometry(720, 660, 210, 60)
        self.loginbutton.setStyleSheet("""
            QPushButton {
                background-color: #002bbd;
                color: white;
                font-size: 18px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)
        self.loginbutton.setCursor(Qt.PointingHandCursor)
        self.loginbutton.clicked.connect(self.begin_login)

        self.guestbutton = QPushButton("Guest mode", self.content)
        self.guestbutton.setGeometry(940, 660, 210, 60)
        self.guestbutton.setStyleSheet("""
            QPushButton {
                background-color: #0055ff;
                color: white;
                font-size: 18px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0080ff;
            }
        """)
        self.guestbutton.setCursor(Qt.PointingHandCursor)
        self.guestbutton.clicked.connect(self.begin_guest_mode)

        #==========================
        #  USERNAME/PASSWORD TEXT
        #==========================
        self.username_text = QLabel("Username:", self.content)
        self.username_text.setGeometry(720, 472, 200, 30)
        self.username_text.setStyleSheet("color: white; font-size: 18px;font-weight: bold; font-family: Bahnschrift;")

        self.password_text = QLabel("Password:", self.content)
        self.password_text.setGeometry(720, 555, 200, 30)
        self.password_text.setStyleSheet("color: white; font-size: 18px;font-weight: bold; font-family: Bahnschrift;")

        self.password_text.setAttribute(Qt.WA_TranslucentBackground, True)
        self.username_text.setAttribute(Qt.WA_TranslucentBackground, True)

        #==========================
        #      HELP BUTTON
        #==========================
        self.helpbutton = QPushButton("Help", self.content)
        self.helpbutton.setGeometry(720, 740, 210, 60)
        self.helpbutton.setStyleSheet("""
            QPushButton {
                background-color: #002bbd;
                color: white;
                font-size: 18px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)
        self.helpbutton.setCursor(Qt.PointingHandCursor)
        self.helpbutton.clicked.connect(self.show_help)

        #==========================
        #      BOOT LOTON
        #==========================
        self.bootloton = QPushButton("Boot LOTON", self.content)
        self.bootloton.setGeometry(780, 700, 210, 60)
        self.bootloton.setStyleSheet(
            """QPushButton {
                background-color: #002bbd;
                color: white;
                font-size: 18px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)
        self.bootloton.setCursor(Qt.PointingHandCursor)
        self.bootloton.clicked.connect(self.BootLOTON)
        self.bootloton.hide()  # Initially hidden, will be shown after login

        #==========================
        #      EXIT BUTTON
        #==========================
        self.exitbutton = QPushButton("Exit", self.content)
        self.exitbutton.setGeometry(940, 740, 210, 60)
        self.exitbutton.setStyleSheet(
            """QPushButton {
                background-color: #002bbd;
                color: white;
                font-size: 18px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)

        self.exitbutton.setCursor(Qt.PointingHandCursor)
        self.exitbutton.clicked.connect(self.begin_exit)

        self.actiondelay = QTimer(self)
        self.actiondelay.setSingleShot(True)
        self.actiondelay.timeout.connect(self.run_pending_action)

        self.loadingicon_timer = QTimer(self)
        self.loadingicon_timer.timeout.connect(self.advance_loading_icon)

        self.loadingicon = QLabel(self.content)
        self.loadingicon.setFixedSize(36, 36)
        self.loadingicon.setAlignment(Qt.AlignCenter)
        self.loadingicon.setStyleSheet("""
            color: white;
            font-size: 26px;
            font-weight: bold;
            background: transparent;
        """)
        self.loadingicon.hide()

    #==========================
    #      LOADING SCREEN
    #==========================
    #A text for a loading screen that will be shown after clicking boot LOTON
        self.loadingscreen = QLabel("Loading LOTON...", self.content)
        self.loadingscreen.setGeometry(0, 0, 1920, 1080)
        self.loadingscreen.setAlignment(Qt.AlignCenter)
        self.loadingscreen.setStyleSheet("QLabel { background-color: black; color: white; font-size: 125px; font-weight: bold; font-family: Bahnschrift; }")
        self.loadingscreen.hide()  # Initially hidden, will be shown after clicking "boot LOTON"

    #==========================
    #      VERSION TEXT
    #==========================
        self.versiontext = QLabel("LOTON OS v1.3.5.5", self.content)
        self.versiontext.setGeometry(5, 1020, 200, 30)
        self.versiontext.setStyleSheet("color: white; font-size: 16px;font-weight: bold; font-family: Bahnschrift;")
        self.versiontext.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    #==========================
    #     DEFINITIONS
    #==========================



    def exitsystem(self):
        main_module = sys.modules.get("LOTON_MAIN") or sys.modules.get("__main__")
        quit_without_shutdown = getattr(main_module, "quit_without_shutdown", None)

        if callable(quit_without_shutdown):
            quit_without_shutdown()
        else:
            self.close()
            QApplication.quit()

    def begin_login(self):
        self.start_delayed_action(self.loginbutton, self.handle_login)

    def begin_guest_mode(self):
        self.start_delayed_action(self.guestbutton, self.handle_guest_mode)

    def begin_exit(self):
        self.start_delayed_action(self.exitbutton, self.exitsystem)

    def start_delayed_action(self, button, action):
        if self._pending_action is not None:
            return

        self._pending_action = action
        self._spinner_index = 0
        self.position_loading_icon(button)
        self.loadingicon.setText(self._spinner_frames[self._spinner_index])
        self.loadingicon.show()
        self.loadingicon.raise_()
        self.set_action_buttons_enabled(False)
        self.loadingicon_timer.start(120)
        self.actiondelay.start(1000)

    def position_loading_icon(self, button):
        x = button.x() + button.width() - self.loadingicon.width() - 12
        y = button.y() + (button.height() - self.loadingicon.height()) // 2
        self.loadingicon.move(x, y)

    def advance_loading_icon(self):
        self._spinner_index = (self._spinner_index + 1) % len(self._spinner_frames)
        self.loadingicon.setText(self._spinner_frames[self._spinner_index])

    def run_pending_action(self):
        action = self._pending_action
        self._pending_action = None

        if callable(action):
            action()

    def stop_loading_feedback(self):
        self.actiondelay.stop()
        self.loadingicon_timer.stop()
        self.loadingicon.hide()
        self.set_action_buttons_enabled(True)

    def set_action_buttons_enabled(self, enabled):
        for button in (
            self.loginbutton,
            self.guestbutton,
            self.helpbutton,
            self.bootloton,
            self.exitbutton,
        ):
            button.setEnabled(enabled)


    def handle_login(self):
        username = self.username_field.text().strip()
        password = self.password_field.text()

        user = Login_screen_userpass.authenticate_user(username, password)

        if user:
            self._authenticated_user = user
            self.stop_loading_feedback()
            self.login_success()
        else:
            self._authenticated_user = None
            self.stop_loading_feedback()
            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password."
            )

    def handle_guest_mode(self):
        self._authenticated_user = {
            "username": "Guest",
            "DisplayName": "Guest",
        }
        self.stop_loading_feedback()
        self.login_success()



    def BootLOTON(self):
        self.loadingscreen.show()
        self.title_bar.hide()
        self.versiontext.hide()
        self.lotonlogo.hide()
        QTimer.singleShot(2000, self.close)


    def login_success(self):
        display_name = (
            self._authenticated_user.get("DisplayName")
            if self._authenticated_user
            else self.username_field.text().strip()
        )

        self.welcomemessage.setText(f"Welcome, {display_name}")

        # Hide login UI
        self.loginbutton.hide()
        self.guestbutton.hide()
        self.helpbutton.hide()
        self.username_field.hide()
        self.password_field.hide()
        self.username_text.hide()
        self.password_text.hide()

        # Show boot button
        self.bootloton.show()

        # Reposition buttons (centered layout after login)
        self.bootloton.setGeometry(835, 520, 210, 60)
        self.exitbutton.setGeometry(835, 600, 210, 60)

        QApplication.processEvents()

        try:
            QMessageBox.information(
                self,
                "Login Successful",
                f"Welcome to LOTON OS, {display_name}."
            )
        except Exception as e:
            print(f"Error showing login success message: {e}")

    def show_help(self):
        QMessageBox.information(
            self,
            "Login Help",
            "To log in, simply click the 'Login' button and you will be logged in, that's it."
        )

_login_window = None


def login_activate():
    global _login_window
    _login_window = Login()
    _login_window.showFullScreen()
    return _login_window

#==========================
#     STANDALONE TEST
#==========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = Login()
    login_window.showFullScreen()
    sys.exit(app.exec())
