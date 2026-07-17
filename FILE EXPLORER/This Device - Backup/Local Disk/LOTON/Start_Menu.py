# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from path import asset_path
import Calculator
import Notepad
import CMD


class StartMenu(QWidget):
    def __init__(self, desktop=None, shutdown_callback=None, app_opened_callback=None):
        super().__init__(desktop)
        self.desktop = desktop
        self.shutdown_callback = shutdown_callback
        self.app_opened_callback = app_opened_callback

        # =========================
        # Start menu PANEL (container)
        # =========================
        self.panel = QWidget(self.desktop)
        self.panel.setGeometry(0, 132, 650, 850)

        # =========================
        # Background
        # =========================
        self.startmenu = QLabel(self.panel)
        st_path = asset_path("Real assets", "resized", "Start Menu resized.png")
        self.startmenu.setPixmap(QPixmap(st_path))
        self.startmenu.setGeometry(0, 0, 650, 850)
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

        self.commandprompttab = QLabel(self.panel)
        cpt_path = asset_path("Real assets", "Start Menu", "Command Prompt tab.png")
        self.commandprompttab.setPixmap(QPixmap(cpt_path))
        self.commandprompttab.setGeometry(71, 469, 402, 67)

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

        # Initially hidden
        self.panel.hide()

        self.startmenu.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Connect events
        self.shutdownbutton.mousePressEvent = self._shutdown_button_press
        self.calculatortab.mousePressEvent = self._calculator_tab_press
        self.notepadtab.mousePressEvent = self._notepad_tab_press
        self.commandprompttab.mousePressEvent = self._command_prompt_tab_press

    # =========================
    # Controls / Methods
    # =========================
    def show_all(self):
        self.panel.show()
        self.panel.raise_()

    def hide_all(self):
        self.panel.hide()

    def _calculator_tab_press(self, event):
        if event.button() == Qt.LeftButton:
            Calculator.turn_on_calculator()
            self.hide_all()
        if callable(self.app_opened_callback):
            self.app_opened_callback()
        event.accept()

    def _notepad_tab_press(self, event):
        if event.button() == Qt.LeftButton:
            Notepad.notepad_activate()
            self.hide_all()
        if callable(self.app_opened_callback):
            self.app_opened_callback()
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
        if callable(self.app_opened_callback):
            self.app_opened_callback()
        event.accept()