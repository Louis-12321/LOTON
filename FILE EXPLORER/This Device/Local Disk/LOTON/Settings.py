# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE.md file for details.
#______________________________________________________________________________________

#region IMPORTS

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QPushButton, QStackedWidget,
    QCheckBox, QComboBox, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainterPath
import sys
from pathlib import Path

import Account_Manager
from Theme_Manager import set_theme, install_theme_sync


WIDTH = 500
HEIGHT = 350
RADIUS = 16

_personalisation_appliers = {}

def register_personalisation_appliers(**appliers):
    _personalisation_appliers.update(appliers)

#endregion

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_position = None
        self.resizing = False

        self.setWindowTitle("Settings")
        self.resize(WIDTH, HEIGHT)
        self.setMinimumSize(700, 450)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.current_theme = "default"

        #region INIT

    
        #===============================
        #============ ROOT =============
        #===============================

        self.root = QWidget(self)
        self.root.setStyleSheet("""
            QWidget {
                background-color: #003eff;
                border-radius: 16px;
            }
        """)

        #===============================
        #========== TITLE BAR ==========
        #===============================

        self.title_bar = QWidget(self.root)
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("""
            background-color: #002bbd;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        """)
        self.title_bar.installEventFilter(self)

        title_layout = QGridLayout(self.title_bar)
        title_layout.setContentsMargins(8, 0, 8, 0)

        title = QLabel("LOTON Settings")
        title.setStyleSheet("color:white; font-size:14px;")

        btn_min = QPushButton("—")
        btn_close = QPushButton("✕")

        for btn in (btn_min, btn_close):
            btn.setFixedSize(28, 24)
            btn.setFocusPolicy(Qt.NoFocus)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0040ff;
                    color: white;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #ff4444;
                }
            """)

        btn_min.clicked.connect(self.showMinimized)
        btn_close.clicked.connect(self.close)

        title_layout.addWidget(title, 0, 0)
        title_layout.addWidget(btn_min, 0, 1)
        title_layout.addWidget(btn_close, 0, 2)
        title_layout.setColumnStretch(0, 1)


        #===============================
        #========= RESIZE GRIP =========
        #===============================

        self.resize_handle = QWidget(self.root)
        self.resize_handle.setFixedSize(18, 18)
        self.resize_handle.setStyleSheet("""
            background-color: #6fa8ff;
            border-radius: 6px;
        """)
        self.resize_handle.setCursor(Qt.SizeFDiagCursor)

        self.update_layout()

        #endregion

        #region GUI
        #===============================
        #======= STACKED WIDGET ========
        #===============================

        self.pages = QStackedWidget(self.root)

        #region Pages

        #============ Home =============
        self.home_page = QWidget()
        self.home_layout = QVBoxLayout(self.home_page)
        self.home_title = QLabel("Settings")
        self.home_title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)

        self.introduction_label = QLabel("Please select a category from the left")
        self.introduction_label.setStyleSheet("""
        color: White;
        font-size: 14px;
                                            
        """)

        self.home_layout.addWidget(self.home_title)
        self.home_layout.addWidget(self.introduction_label)
        self.home_layout.addStretch()
    


        #========= Appearance ==========
        self.appearance_page = QWidget()
        self.appearance_layout = QVBoxLayout(self.appearance_page)
        self.appearance_title = QLabel("Change Themes")
        self.appearance_title.setStyleSheet("""
        color: White;
        font-size: 24px;
        """)

        self.appearance_theme = QComboBox()
        self.appearance_theme.addItems([
            "Default",
            "Dark",
            "Light",
        ])
        self.appearance_theme.setStyleSheet("""
        QComboBox {
        background-color: #006eff;
        color: white;
        border: 2px solid #1100ff;
        border-radius: 7px;
        font-size: 15px;
        }
        QComboBox:hover {
        background-color: #00a6ff;         
        border: 2px solid #006eff;  
        }
        QComboBox::down-arrow {
        image: none;
        }
        QComboBox::drop-down {
        width: 0px                                    
        }
        QComboBox QAbstractItemView {
        background-color: #006eff;
        color: White;
        selection-background-color: #00a6ff;
        border: 2px solid #1100ff;
        border-radius: 5px
        }
    """)

        self.appearance_theme.currentTextChanged.connect(self.theme_changed)


        self.appearance_layout.addWidget(self.appearance_title)
        self.appearance_layout.addWidget(self.appearance_theme)
        self.appearance_layout.addStretch()

        

        #=========== About =============
        self.about_page = QWidget()
        self.about_layout = QVBoxLayout(self.about_page)
        self.about_title = QLabel("About LOTON")
        self.about_title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)

        version_label = QLabel("LOTON Version 1.3.5.0")
        version_label.setStyleSheet("""
            color: white;
            font-size: 14px;
        """)
        creator_label = QLabel("Created by Ur.Average.Louis")
        creator_label.setStyleSheet("""
            color: white;
            font-size: 14px;
        """)

        self.about_layout.addWidget(self.about_title)
        self.about_layout.addWidget(version_label)
        self.about_layout.addWidget(creator_label)
        self.about_layout.addStretch()

        #====== Personalisation =======
        self.personalisation_page = QWidget()

        self.personalisation_layout = QVBoxLayout(
            self.personalisation_page
        )

        self.personalisation_layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        self.personalisation_layout.setSpacing(8)


        #===============================
        #============ STYLES ===========
        #===============================

        button_style = """
        QPushButton {
            background-color: #0040ff;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px;
            font-size: 14px;
            text-align: left;
        }

        QPushButton:hover {
            background-color: #0055ff;
        }

        QPushButton:pressed {
            background-color: #002bbd;
        }
        """

        label_style = """
        QLabel {
            color: white;
            font-size: 14px;
        }
        """

        section_label_style = """
        QLabel {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }
        """

        checkbox_style = """
        QCheckBox {
            color: white;
            font-size: 14px;
            spacing: 8px;
        }

        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 2px solid #6fa8ff;
            border-radius: 4px;
            background-color: #002bbd;
        }

        QCheckBox::indicator:hover {
            border-color: #9bc5ff;
        }

        QCheckBox::indicator:checked {
            background-color: #6fa8ff;
            border-color: #6fa8ff;
        }
        """

        combobox_style = """
        QComboBox {
            background-color: #002bbd;
            color: white;
            border: 2px solid #6fa8ff;
            border-radius: 6px;
            padding: 6px;
            font-size: 14px;
            min-width: 120px;
        }

        QComboBox:hover {
            border-color: #9bc5ff;
        }

        QComboBox::drop-down {
            border: none;
            width: 24px;
        }

        QComboBox QAbstractItemView {
            background-color: #002bbd;
            color: white;
            border: 1px solid #6fa8ff;
            selection-background-color: #0040ff;
            selection-color: white;
        }
        """


        #===============================
        #============= TITLE ===========
        #===============================

        personalisation_title = QLabel("Personalisation")

        personalisation_title.setStyleSheet("""
        QLabel {
            color: white;
            font-size: 24px;
            font-weight: bold;
        }
        """)

        self.personalisation_layout.addWidget(
            personalisation_title
        )

        self.personalisation_layout.addSpacing(12)


        #===============================
        #=========== WALLPAPER =========
        #===============================

        wallpaper_label = QLabel("Wallpaper")
        wallpaper_label.setStyleSheet(section_label_style)

        wallpaper_description = QLabel(
            "Choose the wallpaper shown on the LOTON desktop."
        )

        wallpaper_description.setWordWrap(True)
        wallpaper_description.setStyleSheet(label_style)

        wallpaper_button = QPushButton(
            "Choose Wallpaper"
        )

        wallpaper_button.setStyleSheet(button_style)
        wallpaper_button.setFixedHeight(38)
        wallpaper_button.clicked.connect(self.choose_wallpaper)

        self.personalisation_layout.addWidget(
            wallpaper_label
        )

        self.personalisation_layout.addWidget(
            wallpaper_description
        )

        self.personalisation_layout.addWidget(
            wallpaper_button
        )

        self.personalisation_layout.addSpacing(16)


        #===============================
        #========= DESKTOP ICONS =======
        #===============================

        desktop_label = QLabel("Desktop")
        desktop_label.setStyleSheet(section_label_style)

        show_icons_checkbox = QCheckBox(
            "Show desktop icons"
        )

        show_icons_checkbox.setChecked(True)
        show_icons_checkbox.setStyleSheet(
            checkbox_style
        )
        show_icons_checkbox.stateChanged.connect(self.on_show_icons_changed)

        self.personalisation_layout.addWidget(
            desktop_label
        )

        self.personalisation_layout.addWidget(
            show_icons_checkbox
        )

        self.personalisation_layout.addSpacing(16)


        #===============================
        #============ TASKBAR ==========
        #===============================

        taskbar_label = QLabel("Taskbar")
        taskbar_label.setStyleSheet(section_label_style)

        taskbar_position_label = QLabel(
            "Taskbar position"
        )

        taskbar_position_label.setStyleSheet(
            label_style
        )

        taskbar_position = QComboBox()

        taskbar_position.addItems([
            "Bottom",
            "Top"
        ])

        taskbar_position.setStyleSheet(
            combobox_style
        )

        taskbar_position.setFixedHeight(38)
        taskbar_position.currentTextChanged.connect(self.on_taskbar_position_changed)

        self.personalisation_layout.addWidget(
            taskbar_label
        )

        self.personalisation_layout.addWidget(
            taskbar_position_label
        )

        self.personalisation_layout.addWidget(
            taskbar_position
        )

        self.personalisation_layout.addSpacing(16)


        #===============================
        #======= PROFILE PICTURE =======
        #===============================

        profile_label = QLabel("Profile")
        profile_label.setStyleSheet(section_label_style)

        profile_description = QLabel(
            "Change the profile picture for the current LOTON account."
        )

        profile_description.setWordWrap(True)
        profile_description.setStyleSheet(
            label_style
        )

        profile_button = QPushButton(
            "Change Profile Picture"
        )

        profile_button.setStyleSheet(
            button_style
        )

        profile_button.setFixedHeight(38)
        profile_button.clicked.connect(self.change_profile_picture)

        self.personalisation_layout.addWidget(
            profile_label
        )

        self.personalisation_layout.addWidget(
            profile_description
        )

        self.personalisation_layout.addWidget(
            profile_button
        )

        self.personalisation_layout.addStretch()


        #========== Accounts ==========
        self.accounts_page = QWidget()
        self.accounts_layout = QVBoxLayout(self.accounts_page)
        self.account_title = QLabel("Accounts are managed in the Account Manager")
        self.account_title.setStyleSheet("""
        color: White;
        font-size: 14px;
        font-weight: bold
        """)

        self.button = QPushButton("Open Account Manager")
        self.button.setStyleSheet("""
        QPushButton {
            color: white;
            font-size: 14px;
            background-color: #002fff;
            border: none;
            border-radius: 6px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #0055ff;
        }
    """)
        self.button.clicked.connect(Account_Manager.account_manager_activate)

        self.accounts_layout.addWidget(self.account_title)
        self.accounts_layout.addWidget(self.button)
        self.accounts_layout.addStretch()

        #==============================

        self.pages.setGeometry(
        140,
        36,
        self.root.width() - 140,
        self.root.height() - 36
        ) 

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.appearance_page)
        self.pages.addWidget(self.accounts_page)
        self.pages.addWidget(self.about_page)
        self.pages.addWidget(self.personalisation_page)

        self.pages.setCurrentWidget(self.home_page)

        #endregion

        self.current_theme = self.appearance_theme.currentText()
        install_theme_sync()

        #===============================
        #======= NAVIGATION BAR ========
        #===============================

        #region Navigation Bar

        self.nav_bar = QWidget(self.root)
        self.nav_bar.setGeometry(0, 36, 140, self.root.height() - 36)
        self.nav_bar.setStyleSheet("""
        background-color: #002bbd;
        """)

        self.nav_layout = QVBoxLayout(self.nav_bar)

        self.nav_buttons = {}
        nav_items = [
            ("Home", self.home_page),
            ("Appearance", self.appearance_page),
            ("Accounts", self.accounts_page),
            ("Personalisation", self.personalisation_page),
            ("About", self.about_page)
        ]

        for name, page in nav_items:
            btn = QPushButton(name)
            btn.setFixedHeight(36)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #002bbd;
                    color: white;
                    border: none;
                    text-align: left;
                    padding-left: 12px;
                }

                QPushButton:hover {
                    background-color: #0040ff;
                }
            """)

            btn.clicked.connect(
                lambda checked=False, selected_page=page:
                    self.pages.setCurrentWidget(selected_page)
            )

            self.nav_layout.addWidget(btn)
            self.nav_buttons[name] = btn

        self.nav_layout.addStretch()

        #endregion

        #endregion

#region DEFINITIONS

    def update_layout(self):
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.title_bar.setGeometry(0, 0, self.width(), 36)

        if hasattr(self, "pages"):
            self.pages.setGeometry(
                140,
                36,
                self.root.width() - 140,
                self.root.height() - 36
            )

        self.resize_handle.move(
            self.width() - self.resize_handle.width() - 6,
            self.height() - self.resize_handle.height() - 6
        )

        self.resize_handle.raise_()
        self.apply_mask()

        if hasattr(self, "nav_bar"):
            self.nav_bar.setGeometry(
                0,
                36,
                140,
                self.root.height() - 36
            )

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

    def choose_wallpaper(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Wallpaper",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self._wallpaper_path = file_path
            applier = _personalisation_appliers.get("wallpaper")
            if applier:
                applier(file_path)

    def change_profile_picture(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Change Profile Picture",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self._profile_picture_path = file_path
            applier = _personalisation_appliers.get("profile_picture")
            if applier:
                applier(file_path)

    def on_show_icons_changed(self, state):
        self._show_desktop_icons = bool(state)
        applier = _personalisation_appliers.get("show_icons")
        if applier:
            applier(bool(state))

    def on_taskbar_position_changed(self, position):
        self._taskbar_position = position
        applier = _personalisation_appliers.get("taskbar_position")
        if applier:
            applier(position)

    def theme_changed(self, theme):
        self.current_theme = theme
        set_theme(theme)
#endregion

#region TESTING

#===============================
# ===== STANDALONE TESTING =====
#===============================

_settings_instance = None

def settings_activate():
    global _settings_instance

    if QApplication.instance() is None:
        QApplication(sys.argv)

    if _settings_instance is None:
        _settings_instance = SettingsWindow()

    _settings_instance.show()
    _settings_instance.raise_()
    _settings_instance.activateWindow()


def settings_deactivate():
    if _settings_instance:
        _settings_instance.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())

#endregion