# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
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
        self.startmenu.setGeometry(0, 0, 650, 834)
        self.startmenu.setScaledContents(True)

        # =========================
        # Shutdown button
        # =========================
        self.shutdownbutton = QLabel(self.panel)
        sd_path = asset_path("Real assets", "Icons", "Shutdown button.png")
        self.shutdownbutton.setPixmap(QPixmap(sd_path))
        self.shutdownbutton.setGeometry(7, 750, 62, 62)
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
        # App tabs
        # =========================
        self.calculatortab = QLabel(self.panel)
        ct_path = asset_path("Real assets", "Start Menu", "Calculator tab.png")
        self.calculatortab.setPixmap(QPixmap(ct_path))
        self.calculatortab.setGeometry(71, 223, 402, 67)
        self.calculatortab.setCursor(Qt.PointingHandCursor)

        self.notepadtab = QLabel(self.panel)
        nt_path = asset_path("Real assets", "Start Menu", "Notepad tab.png")
        self.notepadtab.setPixmap(QPixmap(nt_path))
        self.notepadtab.setGeometry(71, 305, 402, 67)
        self.notepadtab.setCursor(Qt.PointingHandCursor)

        self.fileexplorertab = QLabel(self.panel)
        fet_path = asset_path("Real assets", "Start Menu", "File Explorer tab.png")
        self.fileexplorertab.setPixmap(QPixmap(fet_path))
        self.fileexplorertab.setGeometry(71, 387, 402, 67)
        self.fileexplorertab.setCursor(Qt.PointingHandCursor)
        
        self.commandprompttab = QLabel(self.panel)
        cpt_path = asset_path("Real assets", "Start Menu", "Command Prompt tab.png")
        self.commandprompttab.setPixmap(QPixmap(cpt_path))
        self.commandprompttab.setGeometry(71, 469, 402, 67)
        self.commandprompttab.setCursor(Qt.PointingHandCursor)

        self.accountmanagertab = QLabel(self.panel)
        self.accountmanagertab.setGeometry(71, 551, 402, 67)
        am_tab = asset_path("Real assets", "Start Menu", "Account Manager tab.png")
        self.accountmanagertab.setPixmap(QPixmap(am_tab))
        self.accountmanagertab.setAlignment(Qt.AlignCenter)
        self.accountmanagertab.setCursor(Qt.PointingHandCursor)
        self.accountmanagertab.setStyleSheet("""
            background-color: rgba(0, 78, 255, 180);
            color: white;
            border-radius: 14px;
            font-family: bahnschrift;
            font-size: 24px;
            font-weight: 700;
        """)

        self.settingstab = QLabel(self.panel)
        cst_path = asset_path("Real assets", "Start Menu", "Settings tab.png")
        self.settingstab.setPixmap(QPixmap(cst_path))
        self.settingstab.setGeometry(71, 633, 402, 67)
        self.settingstab.setCursor(Qt.PointingHandCursor)


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
        self.calculatortab.raise_()
        self.notepadtab.raise_()
        self.fileexplorertab.raise_()
        self.commandprompttab.raise_()
        self.accountmanagertab.raise_()
        self.settingstab.raise_()

        # Initially hidden
        self.panel.hide()

        self.startmenu.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Connect events
        self.shutdownbutton.mousePressEvent = self._shutdown_button_press
        self.calculatortab.mousePressEvent = self._calculator_tab_press
        self.notepadtab.mousePressEvent = self._notepad_tab_press
        self.fileexplorertab.mousePressEvent = self._file_explorer_tab_press
        self.commandprompttab.mousePressEvent = self._command_prompt_tab_press
        self.accountmanagertab.mousePressEvent = self._account_manager_tab_press
        self.settingstab.mousePressEvent = self._settings_tab_press

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
        

    def _calculator_tab_press(self, event):
        if event.button() == Qt.LeftButton:
            Calculator.turn_on_calculator()
            self.hide_all()
            self._notify_app_opened()
        event.accept()

    def _notepad_tab_press(self, event):
        if event.button() == Qt.LeftButton:
            Notepad.notepad_activate()
            self.hide_all()
            self._notify_app_opened()
        event.accept()

    def _file_explorer_tab_press(self, event):
        if event.button() == Qt.LeftButton:
            File_Explorer.open_file_explorer()
            self.hide_all()
            self._notify_app_opened()
        event.accept()

    def _shutdown_button_press(self, event):
        if event.button() == Qt.LeftButton and callable(self.shutdown_callback):
            self.hide_all()
            self.shutdown_callback()
        event.accept()

    def _command_prompt_tab_press(self, event):
        if event.button() == Qt.LeftButton:
            CMD.cmd_activate()
            self.hide_all()
            self._notify_app_opened()
        event.accept()

    def _account_manager_tab_press(self, event):
        if event.button() == Qt.LeftButton:
            Account_Manager.account_manager_activate()
            self.hide_all()
            self._notify_app_opened()
        event.accept()

    def _settings_tab_press(self, event):
        if event.button() == Qt.LeftButton:
            Settings.settings_activate()
            self.hide_all()
            self._notify_app_opened()
        event.accept()

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
