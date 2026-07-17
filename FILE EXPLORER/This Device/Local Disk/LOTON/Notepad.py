# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE.md file for details.
#______________________________________________________________________________________

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QPushButton, QTextEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainterPath
import sys
from pathlib import Path
from Popup import Popup

sys.path.append(str(Path(__file__).resolve().parents[2]))
from Theme_Manager import install_theme_sync

WIDTH = 480
HEIGHT = 480
RADIUS = 16


class Notepad(QWidget):
    def __init__(self, file_path=None):
        super().__init__()

        # Window setup
        self.setWindowTitle("LOTON Notepad")
        self.resize(WIDTH, HEIGHT)
        self.setMinimumSize(300, 200)

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)

        self.drag_position = QPoint()

        # Root container
        self.root = QWidget(self)
        self.root.setStyleSheet("""
            QWidget {
                background-color: #003eff;
                border-radius: 16px;
            }
        """)


        # Title bar
        self.title_bar = QWidget(self.root)
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("""
            background-color: #002bbd;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        """)

        title_layout = QGridLayout(self.title_bar)
        title_layout.setContentsMargins(8, 0, 8, 0)

        self.title = QLabel("LOTON Notepad")
        self.title.setStyleSheet("color: white; font-size: 18px;")

        btn_min = QPushButton("—")
        btn_close = QPushButton("✕")

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

        title_layout.addWidget(self.title, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        title_layout.addWidget(btn_min, 0, 1)
        title_layout.addWidget(btn_close, 0, 2)
        title_layout.setColumnStretch(0, 1)

        # Toolbar
        self.toolbar = QWidget(self.root)
        self.toolbar.setFixedHeight(36)
        self.toolbar.setStyleSheet("""
            background-color: #426cf5;
            border-radius: 0px;
        """)

        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(8, 4, 8, 4)
        toolbar_layout.setSpacing(6)

        self.top_bar = QLabel()
        self.top_bar.setFixedHeight(28)
        self.top_bar.setStyleSheet("""
            background-color: #426cf5;
            border-radius: 0px;
        """)


        #Save button

        self.save_btn = QPushButton("Save As")
        self.save_btn.setFixedSize(90, 28)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0055ff;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2d73ff;
            }
        """)

        self.save_btn.clicked.connect(self.open_save_popup)

        toolbar_layout.addWidget(self.save_btn)
        toolbar_layout.addStretch()

        # Text area
        self.text_area = QTextEdit(self.root)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background: transparent;
                color: white;
                font-size: 16px;
                border: none;
                padding: 12px;
            }
        """)

        self.text_area.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.text_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        def load_text(self, path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.text_area.setPlainText(content)
            except Exception as e:
                print(f"Error loading file: {e}")

        if file_path:
            load_text(self, file_path)

        # Resize grip (visual)
        self.resize_handle = QWidget(self.root)
        self.resize_handle.setFixedSize(18, 18)
        self.resize_handle.setStyleSheet("""
            background-color: #6fa8ff;
            border-radius: 6px;
        """)
        self.resize_handle.setCursor(Qt.SizeFDiagCursor)

        # Layout
        self.layout = QVBoxLayout(self.root)
        self.layout.setContentsMargins(0, 72, 0, 0)
        self.layout.addWidget(self.text_area)

        self.update_layout()
        install_theme_sync()

    # ---- layout + mask ----
    def update_layout(self):
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.title_bar.setGeometry(0, 0, self.width(), 36)
        self.toolbar.setGeometry(0, 36, self.width(), 36)

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

    # Dragging and resizing
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

        if event.buttons() == Qt.LeftButton and self.title_bar.underMouse():
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.resizing = False

    def open_save_popup(self):
        self.popup = Popup(self)
        self.popup.show()


#LOTON control functions
_notepad_instance = None


def notepad_activate(file_path=None):
    global _notepad_instance
    if QApplication.instance() is None:
        QApplication(sys.argv)
    if _notepad_instance is None:
        _notepad_instance = Notepad(file_path)
    elif file_path:
        _notepad_instance.text_area.setPlainText("")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                _notepad_instance.text_area.setPlainText(f.read())
        except Exception as e:
            print(f"Error loading file: {e}")
    _notepad_instance.show()
    _notepad_instance.raise_()
    _notepad_instance.activateWindow()


def notepad_deactivate():
    if _notepad_instance:
        _notepad_instance.hide()

        if hasattr(_notepad_instance, "popup") and _notepad_instance.popup.isVisible():
            _notepad_instance.popup.hide_all()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad_activate()
    sys.exit(app.exec())
