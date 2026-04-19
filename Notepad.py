# LOTON OS
# Copyright (c) 2026 Louis
# Licensed under the MIT License
#___________________________________________________________________________________________________________________
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QPushButton, QTextEdit
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainterPath
import sys

WIDTH = 480
HEIGHT = 480
RADIUS = 16


class Notepad(QWidget):
    def __init__(self, file_path=None):
        super().__init__()

        # Window setup
        self.setWindowTitle("LOTON Notepad")
        self.resize(WIDTH, HEIGHT)
        self.setMinimumSize(320, 240)

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

        title = QLabel("LOTON Notepad")
        title.setStyleSheet("color: white; font-size: 18px;")

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

        title_layout.addWidget(title, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        title_layout.addWidget(btn_min, 0, 1)
        title_layout.addWidget(btn_close, 0, 2)
        title_layout.setColumnStretch(0, 1)

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
        # Disable automatic line wrapping so very long lines scroll horizontally
        # Use the enum form compatible with this PySide6 binding
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
        self.layout.setContentsMargins(0, 36, 0, 0)
        self.layout.addWidget(self.text_area)

        self.update_layout()

    # ---- layout + mask ----
    def update_layout(self):
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.title_bar.setGeometry(0, 0, self.width(), 36)

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

    #dragging ----
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.title_bar.underMouse():
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.title_bar.underMouse():
            self.move(event.globalPosition().toPoint() - self.drag_position)

    # ---- resizing ----
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
    
    


#LOTON control functions
_notepad_instance = None


def notepad_activate(file_path=None):
    """Show and focus the global Notepad instance."""
    global _notepad_instance
    if QApplication.instance() is None:
        QApplication(sys.argv)
    if _notepad_instance is None:
        _notepad_instance = Notepad(file_path)
    _notepad_instance.show()
    _notepad_instance.raise_()
    _notepad_instance.activateWindow()


def notepad_deactivate():
    """Hide the Notepad window if present."""
    if _notepad_instance:
        _notepad_instance.hide()


def turn_off_notepad():
    """Alias used by the main app to hide/turn off notepad."""
    if _notepad_instance:
        _notepad_instance.hide()

#run standalone
if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad_activate()
    sys.exit(app.exec())
