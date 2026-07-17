# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE.md file for details.
#______________________________________________________________________________________

from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from pathlib import Path


class Taskbar:
    def __init__(self, central, width, height, start_menu,
                 calculator_callback, notepad_callback, cmd_callback,
                 file_explorer_callback, account_manager_callback,
                 settings_callback, shutdown_callback, asset_path_func):
        self.central = central
        self.width = width
        self.height = height
        self.start_menu = start_menu
        self.calculator_callback = calculator_callback
        self.notepad_callback = notepad_callback
        self.cmd_callback = cmd_callback
        self.file_explorer_callback = file_explorer_callback
        self.account_manager_callback = account_manager_callback
        self.settings_callback = settings_callback
        self.shutdown_callback = shutdown_callback
        self.asset_path = asset_path_func

        self.start_menu_open = 0
        self._build()

    def _build(self):
        self.shutdownhitbox = QPushButton(self.central)
        self.shutdownhitbox.setGeometry(7, 900, 62, 62)
        self.shutdownhitbox.setStyleSheet("""
            background-color: transparent;
            border: none;
            color: transparent;
        """)
        self.shutdownhitbox.hide()
        self.shutdownhitbox.setCursor(Qt.PointingHandCursor)
        self.shutdownhitbox.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        if callable(self.shutdown_callback):
            self.shutdownhitbox.clicked.connect(self.shutdown_callback)

        self.cmd_button = QLabel(self.central)
        self.cmd_button.setPixmap(QPixmap(self.asset_path("Real assets", "CMD", "CMD icon.png")))
        self.cmd_button.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.cmd_button.setGeometry(580, 995, 70, 70)
        self.cmd_button.hide()

        self.cmd_hitbox = QPushButton(self.central)
        self.cmd_hitbox.setGeometry(580, 995, 70, 70)
        self.cmd_hitbox.setStyleSheet("""
            background-color: rgba(0,0,0,0);
            border: none;
        """)
        self.cmd_hitbox.setCursor(Qt.PointingHandCursor)
        if callable(self.cmd_callback):
            self.cmd_hitbox.clicked.connect(self.cmd_callback)
        self.cmd_hitbox.hide()

        self.notepad_button = QLabel(self.central)
        self.notepad_button.setPixmap(QPixmap(self.asset_path("Real assets", "Notepad", "Notepad Icon 64x64.png")))
        self.notepad_button.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.notepad_button.setGeometry(465, 995, 70, 70)
        self.notepad_button.hide()

        self.notepad_hitbox = QPushButton(self.central)
        self.notepad_hitbox.setGeometry(465, 995, 70, 70)
        self.notepad_hitbox.setStyleSheet("""
            background-color: rgba(0,0,0,0);
            border: none;
        """)
        self.notepad_hitbox.setCursor(Qt.PointingHandCursor)
        if callable(self.notepad_callback):
            self.notepad_hitbox.clicked.connect(self.notepad_callback)
        self.notepad_hitbox.hide()

        self.calculator_button = QLabel(self.central)
        self.calculator_button.setPixmap(QPixmap(self.asset_path("Real assets", "Calculator", "Calculator button.png")))
        self.calculator_button.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.calculator_button.setGeometry(350, 995, 70, 70)
        self.calculator_button.hide()

        self.calculator_hitbox = QPushButton(self.central)
        self.calculator_hitbox.setGeometry(350, 995, 70, 70)
        self.calculator_hitbox.setStyleSheet("""
            background-color: rgba(0,0,0,0);
            border: none;
        """)
        self.calculator_hitbox.setCursor(Qt.PointingHandCursor)
        if callable(self.calculator_callback):
            self.calculator_hitbox.clicked.connect(self.calculator_callback)
        self.calculator_hitbox.hide()

        self.file_explorer_hitbox = QPushButton(self.central)
        self.file_explorer_hitbox.setGeometry(120, 995, 70, 70)
        self.file_explorer_hitbox.setStyleSheet("""
            background-color: transparent;
            border: none;
            color: transparent;
        """)
        self.file_explorer_hitbox.setCursor(Qt.PointingHandCursor)
        self.file_explorer_hitbox.hide()
        if callable(self.file_explorer_callback):
            self.file_explorer_hitbox.clicked.connect(self.file_explorer_callback)

        self.account_manager_button = QLabel(self.central)
        self.account_manager_button.setPixmap(QPixmap(self.asset_path("Real assets", "Icons", "Account Manager.png")))
        self.account_manager_button.setGeometry(695, 995, 70, 70)
        self.account_manager_button.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.account_manager_button.hide()

        self.account_manager_hitbox = QPushButton(self.central)
        self.account_manager_hitbox.setGeometry(695, 995, 70, 70)
        self.account_manager_hitbox.setStyleSheet("""
            background-color: rgba(0,0,0,0);
            border: none;
        """)
        self.account_manager_hitbox.setCursor(Qt.PointingHandCursor)
        if callable(self.account_manager_callback):
            self.account_manager_hitbox.clicked.connect(self.account_manager_callback)
        self.account_manager_hitbox.hide()

        self.settings_button = QLabel(self.central)
        self.settings_button.setPixmap(QPixmap(self.asset_path("Real assets", "Icons", "Resized", "Settings icon.png")))
        self.settings_button.setGeometry(810, 995, 70, 70)
        self.settings_button.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.settings_button.hide()

        self.settings_hitbox = QPushButton(self.central)
        self.settings_hitbox.setGeometry(810, 995, 70, 70)
        self.settings_hitbox.setStyleSheet("""
            background-color: rgba(0,0,0,0);
            border: none;
        """)
        self.settings_hitbox.setCursor(Qt.PointingHandCursor)
        if callable(self.settings_callback):
            self.settings_hitbox.clicked.connect(self.settings_callback)
        self.settings_hitbox.hide()

        self.startbutton = QLabel(self.central)
        self.startbutton.setPixmap(QPixmap(self.asset_path("Real assets", "Icons", "Resized", "Loton Start Button.png")))
        self.startbutton.setScaledContents(True)
        self.startbutton.setGeometry(10, 995, 70, 70)
        self.startbutton.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.startbutton.setCursor(Qt.PointingHandCursor)
        self.startbutton.mousePressEvent = self._start_button_press
        self.startbutton.show()
        self.startbutton.hide()

        self.folder = QLabel(self.central)
        self.folder.setPixmap(QPixmap(self.asset_path("Real assets", "File Explorer resized.png")))
        self.folder.setGeometry(120, 995, 70, 70)
        self.folder.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.folder.hide()

        self.Loton_store = QLabel(self.central)
        self.Loton_store.setPixmap(QPixmap(self.asset_path("Real assets", "Icons", "Resized", "Loton Store.png")))
        self.Loton_store.setGeometry(230, 995, 70, 70)
        self.Loton_store.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.Loton_store.hide()

        self.taskbar = QLabel(self.central)
        self.taskbar.setPixmap(QPixmap(self.asset_path("Real assets", "Taskbar.png")))
        self.taskbar.setGeometry(0, self.height - 96, self.width, 96)
        self.taskbar.hide()

    def _start_button_press(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_start_menu()
        event.accept()

    def toggle_start_menu(self):
        if self.start_menu_open == 0:
            self.start_menu.show_all()
            self.start_menu_open = 1
        else:
            self.start_menu.hide_all()
            self.start_menu_open = 0

    def on_app_opened(self):
        self.start_menu_open = 0

    def show_all(self):
        self.taskbar.show()
        self.startbutton.show()
        self.folder.show()
        self.account_manager_button.show()
        self.account_manager_hitbox.show()
        self.notepad_button.show()
        self.notepad_hitbox.show()
        self.calculator_button.show()
        self.calculator_hitbox.show()
        self.file_explorer_hitbox.show()
        self.Loton_store.show()
        self.cmd_button.show()
        self.cmd_hitbox.show()
        self.settings_button.show()
        self.settings_hitbox.show()
        self.shutdownhitbox.show()

        self.taskbar.raise_()
        self.startbutton.raise_()
        self.folder.raise_()
        self.account_manager_button.raise_()
        self.account_manager_hitbox.raise_()
        self.Loton_store.raise_()
        self.notepad_button.raise_()
        self.calculator_button.raise_()
        self.notepad_hitbox.raise_()
        self.calculator_hitbox.raise_()
        self.file_explorer_hitbox.raise_()
        self.settings_button.raise_()
        self.settings_hitbox.raise_()
        self.cmd_button.raise_()
        self.cmd_hitbox.raise_()

    def apply_position(self, position):
        tb_height = 96
        icon_size = 70
        gap = 110

        horiz_items = [
            (self.startbutton, None),
            (self.folder, self.file_explorer_hitbox),
            (self.Loton_store, None),
            (self.calculator_button, self.calculator_hitbox),
            (self.notepad_button, self.notepad_hitbox),
            (self.cmd_button, self.cmd_hitbox),
            (self.account_manager_button, self.account_manager_hitbox),
            (self.settings_button, self.settings_hitbox),
        ]

        if position == "Bottom":
            self.taskbar.setGeometry(0, self.height - tb_height, self.width, tb_height)
            base_y = self.height - tb_height + 13
            for i, (label, hitbox) in enumerate(horiz_items):
                x = 10 + i * gap
                label.setGeometry(x, base_y, icon_size, icon_size)
                if hitbox:
                    hitbox.setGeometry(x, base_y, icon_size, icon_size)
            self.shutdownhitbox.setGeometry(7, self.height - tb_height - 50, 62, 62)
            self.start_menu.panel.setGeometry(0, self.height - tb_height - 834, 650, 834)

        elif position == "Top":
            self.taskbar.setGeometry(0, 0, self.width, tb_height)
            base_y = 13
            for i, (label, hitbox) in enumerate(horiz_items):
                x = 10 + i * gap
                label.setGeometry(x, base_y, icon_size, icon_size)
                if hitbox:
                    hitbox.setGeometry(x, base_y, icon_size, icon_size)
            self.shutdownhitbox.setGeometry(7, tb_height + 10, 62, 62)
            self.start_menu.panel.setGeometry(0, tb_height, 650, 834)

        elif position == "Left":
            self.taskbar.setGeometry(0, 0, tb_height, self.height)
            base_x = 13
            base_y = 100
            step = 90
            for i, (label, hitbox) in enumerate(horiz_items):
                y = base_y + i * step
                label.setGeometry(base_x, y, icon_size, icon_size)
                if hitbox:
                    hitbox.setGeometry(base_x, y, icon_size, icon_size)
            self.shutdownhitbox.setGeometry(7, self.height - 70, 62, 62)

        elif position == "Right":
            self.taskbar.setGeometry(self.width - tb_height, 0, tb_height, self.height)
            base_x = self.width - tb_height + 13
            base_y = 100
            step = 90
            for i, (label, hitbox) in enumerate(horiz_items):
                y = base_y + i * step
                label.setGeometry(base_x, y, icon_size, icon_size)
                if hitbox:
                    hitbox.setGeometry(base_x, y, icon_size, icon_size)
            self.shutdownhitbox.setGeometry(self.width - 70, self.height - 70, 62, 62)

    def apply_show_icons(self, show):
        labels = [self.folder, self.calculator_button, self.notepad_button, self.cmd_button,
                  self.account_manager_button, self.settings_button, self.Loton_store]
        hitboxes = [self.file_explorer_hitbox, self.calculator_hitbox, self.notepad_hitbox,
                    self.cmd_hitbox, self.settings_hitbox, self.account_manager_hitbox]
        for w in labels:
            if show:
                w.show()
            else:
                w.hide()
        for w in hitboxes:
            if show:
                w.show()
            else:
                w.hide()
