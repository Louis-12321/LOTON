# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________
#region IMPORTS
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainterPath
from PySide6.QtWidgets import(QApplication, QLabel, QLineEdit, QPushButton, 
QScrollArea, QVBoxLayout, QHBoxLayout, QWidget)
import Login_screen_userpass

sys.path.append(str(Path(__file__).resolve().parents[2]))
from Theme_Manager import install_theme_sync

WIDTH = 580
HEIGHT = 720
RADIUS = 16

#endregion

_account_manager_instance = None


class AccountManager(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_position = None
        self.selected_username = None
        self.resizing = False

        self.setWindowTitle("LOTON Account Manager")
        self.resize(WIDTH, HEIGHT)
        self.setMinimumSize(560, 640)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        

        #region GUI

        self.root = QWidget(self)
        self.root.setStyleSheet("""
            QWidget {
                background-color: #003eff;
                border-radius: 16px;
            }
        """)

        self.main_layout = QVBoxLayout(self.root)
        self.main_layout.setContentsMargins(8, 6, 8, 8)
        self.main_layout.setSpacing(8)

        self.title_bar = QWidget(self.root)
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("""
            background-color: #002bbd;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        """)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(8, 0, 8, 0)

        title = QLabel("LOTON Account Manager")
        title.setStyleSheet("color: white; font-size: 16px; font-family: bahnschrift;")

        btn_min = QPushButton("-")
        btn_close = QPushButton("x")
        for btn in (btn_min, btn_close):
            btn.setFixedSize(28, 24)
            btn.setFocusPolicy(Qt.NoFocus)
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

        btn_min.clicked.connect(self.hide)
        btn_close.clicked.connect(self.hide)

        title_layout.addWidget(title)
        title_layout.addStretch(1)
        title_layout.addWidget(btn_min)
        title_layout.addWidget(btn_close)

        self.info_label = QLabel("Create, delete and update your LOTON accounts")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("""
            color: white;
            font-family: bahnschrift;
            font-size: 13px;
            padding: 4px 8px;
        """)

        self.username_input = QLineEdit()
        self.display_name_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        for widget, placeholder in (
            (self.username_input, "Username"),
            (self.display_name_input, "Display Name"),
            (self.password_input, "Password"),
        ):
            widget.setPlaceholderText(placeholder)
            widget.setStyleSheet("""
                QLineEdit {
                    background-color: #0058ff;
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 72);
                    border-radius: 10px;
                    padding: 8px 10px;
                    font-family: bahnschrift;
                    font-size: 13px;
                }
            """)

        self.create_button = QPushButton("Create Account")
        self.delete_button = QPushButton("Delete Selected")
        self.refresh_button = QPushButton("Refresh accounts")

        for button in (self.create_button, self.delete_button, self.refresh_button):
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #0078ff;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 8px 12px;
                    font-family: bahnschrift;
                    font-size: 13px;
                    font-weight: 700;
                }
                QPushButton:hover {
                    background-color: #0066ff;
                }
            """)

        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 12px;
                font-family: bahnschrift;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            color: #cddfff;
            font-family: bahnschrift;
            font-size: 12px;
            padding: 2px 8px;
        """)

        button_row = QHBoxLayout()
        button_row.setSpacing(8)
        button_row.addWidget(self.create_button)
        button_row.addWidget(self.delete_button)
        button_row.addWidget(self.refresh_button)

        # --- Update Account Section ---
        self.update_section_label = QLabel("Update Selected Account")
        self.update_section_label.setStyleSheet("""
            color: white;
            font-family: bahnschrift;
            font-size: 13px;
            padding: 4px 8px;
            font-weight: 700;
        """)
        self.update_section_label.hide()

        self.current_password_input = QLineEdit()
        self.current_password_input.setPlaceholderText("Current Password (required to update)")
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setStyleSheet("""
            QLineEdit {
                background-color: #0058ff;
                color: white;
                border: 1px solid rgba(255, 255, 255, 72);
                border-radius: 10px;
                padding: 8px 10px;
                font-family: bahnschrift;
                font-size: 13px;
            }
        """)

        self.new_username_input = QLineEdit()
        self.new_username_input.setPlaceholderText("New Username (leave blank to keep current)")
        self.new_username_input.setStyleSheet("""
            QLineEdit {
                background-color: #0058ff;
                color: white;
                border: 1px solid rgba(255, 255, 255, 72);
                border-radius: 10px;
                padding: 8px 10px;
                font-family: bahnschrift;
                font-size: 13px;
            }
        """)

        self.new_display_name_input = QLineEdit()
        self.new_display_name_input.setPlaceholderText("New Display Name (leave blank to keep current)")
        self.new_display_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #0058ff;
                color: white;
                border: 1px solid rgba(255, 255, 255, 72);
                border-radius: 10px;
                padding: 8px 10px;
                font-family: bahnschrift;
                font-size: 13px;
            }
        """)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("New Password (leave blank to keep current)")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setStyleSheet("""
            QLineEdit {
                background-color: #0058ff;
                color: white;
                border: 1px solid rgba(255, 255, 255, 72);
                border-radius: 10px;
                padding: 8px 10px;
                font-family: bahnschrift;
                font-size: 13px;
            }
        """)

        self.update_button = QPushButton("Update Account")
        self.update_button.setCursor(Qt.PointingHandCursor)
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: #0078ff;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 12px;
                font-family: bahnschrift;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #0066ff;
            }
        """)
        self.update_button.setEnabled(False)

        self.user_list_area = QScrollArea()
        self.user_list_area.setWidgetResizable(True)
        self.user_list_area.setStyleSheet("""
            QScrollArea {
                background: #003eff;
                border: none;
            }
        """)

        #endregion

        #region ADDWIDGET

        self.user_list_container = QWidget()
        self.user_list_layout = QVBoxLayout(self.user_list_container)
        self.user_list_layout.setContentsMargins(0, 0, 0, 0)
        self.user_list_layout.setSpacing(8)
        self.user_list_area.setWidget(self.user_list_container)

        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.info_label)
        self.main_layout.addWidget(self.username_input)
        self.main_layout.addWidget(self.display_name_input)
        self.main_layout.addWidget(self.password_input)
        self.main_layout.addLayout(button_row)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.update_section_label)
        self.main_layout.addWidget(self.current_password_input)
        self.main_layout.addWidget(self.new_username_input)
        self.main_layout.addWidget(self.new_display_name_input)
        self.main_layout.addWidget(self.new_password_input)
        self.main_layout.addWidget(self.update_button)
        self.main_layout.addWidget(self.user_list_area, 1)

        self.create_button.clicked.connect(self.create_account)
        self.delete_button.clicked.connect(self.delete_selected_account)
        self.refresh_button.clicked.connect(self.refresh_user_list)
        self.update_button.clicked.connect(self.update_account)

        #endregion

        #region RESIZE

        # Resize grip (visual)
        self.resize_handle = QWidget(self.root)
        self.resize_handle.setFixedSize(18, 18)
        self.resize_handle.setStyleSheet("""
            background-color: #6fa8ff;
            border-radius: 6px;
        """)
        self.resize_handle.setCursor(Qt.SizeFDiagCursor)

        self.update_layout()
        self.refresh_user_list()
        install_theme_sync()

        #endregion

#region DEFINITIONS
    def update_layout(self):
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.title_bar.setGeometry(0, 0, self.width() - 16, 36)
        self.resize_handle.move(
            self.width() - self.resize_handle.width() - 6,
            self.height() - self.resize_handle.height() - 6
        )
        self.apply_mask()

    def apply_mask(self):
        path = QPainterPath()
        path.addRoundedRect(self.rect(), RADIUS, RADIUS)
        self.setMask(path.toFillPolygon().toPolygon())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_layout()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.resize_handle.underMouse():
                self.resizing = True
                self.resize_start = event.globalPosition().toPoint()
                self.start_size = self.size()
                return
            if self.title_bar.underMouse():
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if getattr(self, "resizing", False):
            delta = event.globalPosition().toPoint() - self.resize_start
            new_w = max(self.minimumWidth(), self.start_size.width() + delta.x())
            new_h = max(self.minimumHeight(), self.start_size.height() + delta.y())
            self.resize(new_w, new_h)
            return

        if event.buttons() == Qt.LeftButton and self.title_bar.underMouse() and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.drag_position = None

    def clear_form(self):
        self.username_input.clear()
        self.display_name_input.clear()
        self.password_input.clear()
        self.current_password_input.clear()
        self.new_username_input.clear()
        self.new_display_name_input.clear()
        self.new_password_input.clear()

    def set_status(self, text, color="#d2efff"):
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"""
            color: {color};
            font-family: bahnschrift;
            font-size: 12px;
            padding: 2px 8px;
        """)

    def refresh_user_list(self):
        while self.user_list_layout.count():
            item = self.user_list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        users = Login_screen_userpass.get_all_users()

        for user in users:
            row = QPushButton(f"{user['username']}   |   {user['DisplayName']}")
            row.setCursor(Qt.PointingHandCursor)
            row.setStyleSheet(self._row_style(user["username"] == self.selected_username))
            row.clicked.connect(
                lambda _checked=False, username=user["username"]: self.select_user(username)
            )
            self.user_list_layout.addWidget(row)

        self.user_list_layout.addStretch(1)
        self.delete_button.setEnabled(self.selected_username is not None)
        self.update_button.setEnabled(self.selected_username is not None)

    def _row_style(self, selected):
        if selected:
            return """
                QPushButton {
                    background-color: rgba(157, 210, 255, 95);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    text-align: left;
                    padding: 10px 14px;
                    font-family: bahnschrift;
                    font-size: 13px;
                    font-weight: 700;
                }
            """

        return """
            QPushButton {
                background-color: rgba(0, 43, 189, 150);
                color: white;
                border: none;
                border-radius: 10px;
                text-align: left;
                padding: 10px 14px;
                font-family: bahnschrift;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(157, 210, 255, 80);
            }
        """

    def select_user(self, username):
        self.selected_username = username
        self.refresh_user_list()
        self.set_status(f"Selected account: {username}")
        # Show update section
        self.update_section_label.show()

    def create_account(self):
        username = self.username_input.text().strip()
        display_name = self.display_name_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not display_name or not password:
            self.set_status("Fill in username, display name, and password first.", "#ffd7d7")
            return

        if Login_screen_userpass.username_exists(username):
            self.set_status("That username already exists.", "#ffd7d7")
            return

        Login_screen_userpass.add_user_data(username, display_name, password)
        self.selected_username = username
        self.clear_form()
        self.refresh_user_list()
        self.set_status(f"Created account: {username}", "#bfffd4")

    def update_account(self):
        if not self.selected_username:
            self.set_status("Select an account to update.", "#ffd7d7")
            return

        current_password = self.current_password_input.text().strip()
        if not current_password:
            self.set_status("Enter the current password to verify.", "#ffd7d7")
            return

        # Verify current password
        user = Login_screen_userpass.authenticate_user(self.selected_username, current_password)
        if not user:
            self.set_status("Incorrect current password.", "#ffd7d7")
            return

        new_username = self.new_username_input.text().strip()
        new_display_name = self.new_display_name_input.text().strip()
        new_password = self.new_password_input.text().strip()

        if not new_username and not new_display_name and not new_password:
            self.set_status("Enter at least one new value to update.", "#ffd7d7")
            return

        # Check if new username already exists
        if new_username and new_username != self.selected_username:
            if Login_screen_userpass.username_exists(new_username):
                self.set_status("That username already exists.", "#ffd7d7")
                return

        # Perform update directly in JSON to preserve all fields (theme, isAdmin, etc.)
        data = Login_screen_userpass.load_users_dict()
        for uid, u in data.items():
            if u["username"] == self.selected_username:
                if new_username:
                    data[uid]["username"] = new_username
                if new_display_name:
                    data[uid]["DisplayName"] = new_display_name
                if new_password:
                    data[uid]["password"] = new_password
                break

        Login_screen_userpass.save_users_dict(data)

        final_username = new_username if new_username else self.selected_username
        self.selected_username = final_username
        self.clear_form()
        self.refresh_user_list()
        self.set_status(f"Updated account: {final_username}", "#bfffd4")

    def delete_selected_account(self):
        if not self.selected_username:
            self.set_status("Select an account to delete.", "#ffd7d7")
            return

        Login_screen_userpass.delete_user_data(self.selected_username)
        deleted_username = self.selected_username
        self.selected_username = None
        self.update_section_label.hide()
        self.clear_form()
        self.refresh_user_list()
        self.set_status(f"Deleted account: {deleted_username}", "#ffd7d7")

#endregion

#region TESTING

def account_manager_activate():
    global _account_manager_instance

    if QApplication.instance() is None:
        QApplication(sys.argv)

    if _account_manager_instance is None:
        _account_manager_instance = AccountManager()

    _account_manager_instance.show()
    _account_manager_instance.raise_()
    _account_manager_instance.activateWindow()


def account_manager_deactivate():
    if _account_manager_instance:
        _account_manager_instance.hide()


def account_manager_toggle():
    global _account_manager_instance
    if QApplication.instance() is None:
        QApplication(sys.argv)
    if _account_manager_instance is None:
        _account_manager_instance = AccountManager()
    if _account_manager_instance.isVisible():
        _account_manager_instance.hide()
    else:
        _account_manager_instance.show()
        _account_manager_instance.raise_()
        _account_manager_instance.activateWindow()


#endregion
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    account_manager_activate()
    sys.exit(app.exec())
