# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from path import asset_path
import Calculator
import Notepad
import CMD
import File_Explorer
import Account_Manager
import Settings


class StartMenu(QWidget):
    def __init__(self, desktop=None, shutdown_callback=None, app_opened_callback=None):
        super().__init__(desktop)
        self.desktop = desktop
        self.shutdown_callback = shutdown_callback
        self.app_opened_callback = app_opened_callback

        #region GUI

        # =========================
        # Start menu PANEL (container)
        # =========================
        self.panel = QWidget(self.desktop)
        self.panel.setGeometry(0, 150, 650, 834)

        # =========================
        # Background
        # =========================
        self.startmenu = QLabel(self.panel)
        st_path = asset_path("Real assets", "resized", "Start Menu resized.png")
        self.startmenu.setPixmap(QPixmap(st_path))
        self.startmenu.setGeometry(0, 0, 576, 834)
        self.startmenu.setScaledContents(True)

        # =========================
        # Shutdown button
        # =========================
        self.shutdownbutton = QLabel(self.panel)
        sd_path = asset_path("Real assets", "Icons", "Shutdown button.png")
        self.shutdownbutton.setPixmap(QPixmap(sd_path))
        self.shutdownbutton.setGeometry(5, 750, 62, 62)
        self.shutdownbutton.setCursor(Qt.PointingHandCursor)

        # =========================
        # USER text
        # =========================
        self.usertext = QLabel("USER", self.panel)
        self.usertext.setGeometry(88, 30, 138, 47)
        self.usertext.setAlignment(Qt.AlignCenter)
        self.usertext.setStyleSheet("color: white; font-size: 53px;")

        # =========================
        # User picture
        # =========================
        self.userpic = QLabel(self.panel)
        up_path = asset_path("Real assets", "Icons", "User pic.png")
        self.userpic.setPixmap(QPixmap(up_path))
        self.userpic.setGeometry(238, 15, 144, 144)

        # =========================
        # Apps label
        # =========================
        self.appstext = QLabel("Apps", self.panel)
        self.appstext.setGeometry(71, 194, 61, 27)
        self.appstext.setAlignment(Qt.AlignCenter)
        self.appstext.setStyleSheet("color: white; font-size: 25px;")

        # =========================
        # App tabs (programmatic)
        # =========================
        tab_style = """
            QPushButton {
                background-color: rgba(0, 78, 255, 180);
                color: white;
                border-radius: 0px;
                font-family: bahnschrift;
                font-size: 22px;
                font-weight: 700;
                text-align: left;
                padding-left: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 255, 220);
            }
        """

        def _tab_icon(path):
            pm = QPixmap(path)
            if pm.isNull():
                return QIcon(), QSize(42, 42)
            scaled = pm.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return QIcon(scaled), scaled.size()

        def make_tab(text, icon_path, geometry, callback):
            btn = QPushButton(self.panel)
            btn.setGeometry(*geometry)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(tab_style)
            icon, isize = _tab_icon(icon_path)
            btn.setIcon(icon)
            btn.setIconSize(isize)
            btn.setText("   " + text)
            btn.clicked.connect(callback)
            return btn

        self.calculatortab = make_tab(
            "Calculator", asset_path("Real assets", "Calculator", "Calculator button.png"),
            (71, 223, 402, 67), self._calculator_tab_press)

        self.notepadtab = make_tab(
            "Notepad", asset_path("Real assets", "Notepad", "Notepad Icon 64x64.png"),
            (71, 305, 402, 67), self._notepad_tab_press)

        self.fileexplorertab = make_tab(
            "File Explorer", asset_path("Real assets", "File Explorer resized.png"),
            (71, 387, 402, 67), self._file_explorer_tab_press)

        self.commandprompttab = make_tab(
            "Command Prompt", asset_path("Real assets", "CMD", "CMD icon.png"),
            (71, 469, 402, 67), self._command_prompt_tab_press)

        self.accountmanagertab = make_tab(
            "Account Manager", asset_path("Real assets", "Icons", "Account Manager.png"),
            (71, 551, 402, 67), self._account_manager_tab_press)

        self.settingstab = make_tab(
            "Settings", asset_path("Real assets", "Icons", "Resized", "Settings icon.png"),
            (71, 633, 402, 67), self._settings_tab_press)


        # =========================
        # Search Bar
        # =========================

        self.searchbar = QLineEdit(self.panel)
        self.searchbar.setGeometry(75, 760, 350, 62)

        self.searchbar.setStyleSheet("""
            QLineEdit {
                color: #6fa0ff;
                background-color: #0380fc;
                border: 2px solid white;
                font-size: 25px;
                font-family: Bahnschrift;
                padding: 12px;
                border-radius: 10px;
            }
        """)
        self.searchbar.setPlaceholderText("Search...")
        self.searchbar.returnPressed.connect(self.search_entered)


        # =========================
        # Z-order inside panel
        # =========================
        self.startmenu.lower()
        self.shutdownbutton.raise_()
        self.usertext.raise_()
        self.userpic.raise_()
        self.appstext.raise_()

        # Initially hidden
        self.panel.hide()

        self.startmenu.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Connect events
        self.shutdownbutton.mousePressEvent = self._shutdown_button_press

    #endregion

    # =========================
    # Controls / Methods
    # =========================
    #region DEFS
    def show_all(self):
        self.panel.show()
        self.panel.raise_()

    def hide_all(self):
        self.panel.hide()

    def _notify_app_opened(self):
        if callable(self.app_opened_callback):
            self.app_opened_callback()
        

    def _calculator_tab_press(self):
        Calculator.turn_on_calculator()
        self.hide_all()
        self._notify_app_opened()

    def _notepad_tab_press(self):
        Notepad.notepad_activate()
        self.hide_all()
        self._notify_app_opened()

    def _file_explorer_tab_press(self):
        File_Explorer.open_file_explorer()
        self.hide_all()
        self._notify_app_opened()

    def _shutdown_button_press(self, event):
        if event.button() == Qt.LeftButton and callable(self.shutdown_callback):
            self.hide_all()
            self.shutdown_callback()
        event.accept()

    def _command_prompt_tab_press(self):
        CMD.cmd_activate()
        self.hide_all()
        self._notify_app_opened()

    def _account_manager_tab_press(self):
        Account_Manager.account_manager_activate()
        self.hide_all()
        self._notify_app_opened()

    def _settings_tab_press(self):
        Settings.settings_activate()
        self.hide_all()
        self._notify_app_opened()

    def click_outside_close(self, global_pos):
        if self.panel.isVisible():
            local_pos = self.panel.mapFromGlobal(global_pos)
            
            if not self.panel.rect().contains(local_pos):
                self.hide_all()

    def search_entered(self):
        query = self.searchbar.text().strip().lower()

        if "calc" in query:
            Calculator.turn_on_calculator()
            self.hide_all()
            self._notify_app_opened()
            self.searchbar.clear()

        elif "note" in query:
            Notepad.notepad_activate()
            self.hide_all()
            self._notify_app_opened()
            self.searchbar.clear()

        elif "file ex" in query:
            File_Explorer.open_file_explorer()
            self.hide_all()
            self._notify_app_opened()
            self.searchbar.clear()

        elif "command prom" in query or query == "cmd" or query == "terminal" or query == "console":
            CMD.cmd_activate()
            self.hide_all()
            self._notify_app_opened()
            self.searchbar.clear()

        elif "setti" in query:
            Settings.settings_activate()
            self.hide_all()
            self._notify_app_opened()
            self.searchbar.clear()
        
        elif "account man" in query:
            Account_Manager.account_manager_activate()
            self.hide_all()
            self._notify_app_opened()
            self.searchbar.clear()

        else:
            print("Not found")
            self.hide_all()
            self.searchbar.clear()

    #endregion
