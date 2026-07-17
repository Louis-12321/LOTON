from pathlib import Path

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from path import asset_path


class FileItem(QWidget):
    def __init__(self, name, icon_path, parent=None):
        super().__init__(parent)

        self.setFixedSize(120, 120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        icon_label = QLabel(self)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedHeight(64)

        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon_label.setPixmap(
                pixmap.scaled(
                    56,
                    56,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

        text_label = QLabel(name, self)
        text_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("""
            color: white;
            font-size: 13px;
            background: transparent;
        """)

        self.setStyleSheet("""
            QWidget {
                background: transparent;
                border-radius: 10px;
            }
            QWidget:hover {
                background: rgba(255, 255, 255, 0.12);
            }
        """)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)


class FileExplorer(QWidget):
    ITEM_WIDTH = 120
    ITEM_HEIGHT = 120

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(478, 240, 964, 601)

        self._drag_offset = QPoint()
        self._dragging = False
        self._current_columns = 0
        self._items = []

        self.window_label = QLabel(self)
        self.window_label.setGeometry(0, 0, 964, 601)
        self.window_label.setPixmap(
            QPixmap(asset_path("Real assets", "Window", "Window.png"))
        )
        self.window_label.setScaledContents(True)
        self.window_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.title_bar = QWidget(self)
        self.title_bar.setGeometry(0, 0, 964, 36)
        self.title_bar.setStyleSheet("""
            background-color: rgba(0, 43, 189, 215);
            border: none;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        """)

        title_layout = QGridLayout(self.title_bar)
        title_layout.setContentsMargins(12, 0, 8, 0)
        title_layout.setHorizontalSpacing(6)

        self.title_label = QLabel("LOTON File Explorer")
        self.title_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600;")

        self.min_button = QPushButton("-")
        self.close_button = QPushButton("x")

        for btn in (self.min_button, self.close_button):
            btn.setFixedSize(28, 24)
            btn.setFocusPolicy(Qt.NoFocus)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0040ff;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #ff4444;
                }
            """)

        self.min_button.clicked.connect(self.hide)
        self.close_button.clicked.connect(self.hide)

        title_layout.addWidget(self.title_label, 0, 0)
        title_layout.addWidget(self.min_button, 0, 1)
        title_layout.addWidget(self.close_button, 0, 2)
        title_layout.setColumnStretch(0, 1)

        self.content_area = QScrollArea(self)
        self.content_area.setGeometry(24, 56, 916, 520)
        self.content_area.setWidgetResizable(True)
        self.content_area.setFrameShape(QScrollArea.NoFrame)
        self.content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.content_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        self.icon_layout = QGridLayout(self.content_widget)
        self.icon_layout.setContentsMargins(12, 12, 12, 12)
        self.icon_layout.setHorizontalSpacing(12)
        self.icon_layout.setVerticalSpacing(12)
        self.icon_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.content_area.setWidget(self.content_widget)

        self._load_directory_entries()
        self._relayout_items()

        self.title_bar.raise_()

    def _load_directory_entries(self):
        local_disk_dir = Path(__file__).resolve().parents[1]
        folder_icon = asset_path("Real assets", "File Explorer", "Folder icon.png")
        file_icon = asset_path("Real assets", "File Explorer", "File icon.png")

        entries = sorted(local_disk_dir.iterdir(), key=lambda entry: (entry.is_file(), entry.name.lower()))
        self._items = [
            FileItem(entry.name, folder_icon if entry.is_dir() else file_icon, self.content_widget)
            for entry in entries
        ]

    def _clear_layout(self):
        while self.icon_layout.count():
            item = self.icon_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(self.content_widget)

    def _relayout_items(self):
        if not self._items:
            return

        available_width = max(1, self.content_area.viewport().width() - 24)
        columns = max(1, available_width // (self.ITEM_WIDTH + self.icon_layout.horizontalSpacing()))
        if columns == self._current_columns and self.icon_layout.count() == len(self._items):
            return

        self._current_columns = columns
        self._clear_layout()

        for index, widget in enumerate(self._items):
            row = index // columns
            column = index % columns
            self.icon_layout.addWidget(widget, row, column)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.window_label.resize(self.size())
        self.title_bar.resize(self.width(), 36)
        self.content_area.setGeometry(24, 56, self.width() - 48, self.height() - 80)
        self._relayout_items()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.title_bar.geometry().contains(event.position().toPoint()):
            self._dragging = True
            self._drag_offset = event.globalPosition().toPoint() - self.pos()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_offset)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        super().mouseReleaseEvent(event)
