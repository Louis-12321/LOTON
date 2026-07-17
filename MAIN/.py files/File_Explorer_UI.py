# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainterPath, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from path import asset_path, resource_path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import Theme_Manager

WIDTH = 1000
HEIGHT = 700
RADIUS = 16


class FileItemHitbox(QWidget):
    def __init__(self, explorer, index, item_path, item_name, file_type, x, y, w, h):
        super().__init__(explorer.file_area)
        self.explorer = explorer
        self.index = index
        self.item_path = item_path
        self.item_name = item_name
        self.file_type = file_type
        self.is_renaming = False

        self.setGeometry(x, y, w, h)
        self.setCursor(Qt.PointingHandCursor)
        self._build_contents()
        self.update_selection_style(False)
        self.show()

    def _build_contents(self):
        icon_size = self.explorer._scaled(60)
        icon_panel_size = self.explorer._scaled(84)
        icon_panel_y = self.explorer._scaled(8)
        name_y = icon_panel_y + icon_panel_size + self.explorer._scaled(10)
        name_height = self.explorer._scaled(32)
        name_width = self.width() - self.explorer._scaled(18)

        if self.file_type == "folder":
            icon_path = asset_path("Real Assets", "File Explorer", "Folder icon.png")
            if Theme_Manager.CURRENT_THEME == "Dark":
                dark = asset_path("Real Assets", "Settings", "Themes", "File Explorer", "Folder icon.png")
                if Path(dark).exists():
                    icon_path = dark
        else:
            icon_path = asset_path("Real Assets", "File Explorer", "File icon.png")

        self.icon_panel = QFrame(self)
        self.icon_panel.setGeometry(
            (self.width() - icon_panel_size) // 2,
            icon_panel_y,
            icon_panel_size,
            icon_panel_size
        )

        self.icon = QLabel(self.icon_panel)
        self.icon.setGeometry(
            (icon_panel_size - icon_size) // 2,
            (icon_panel_size - icon_size) // 2,
            icon_size,
            icon_size
        )
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        pixmap = QPixmap(icon_path)
        self.icon.setPixmap(
            pixmap.scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        self.name_label = QLabel(self)
        self.name_label.setGeometry(
            (self.width() - name_width) // 2,
            name_y,
            name_width,
            name_height
        )
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.name_label.setToolTip(self.item_name)
        self.name_label.setText(self.item_name)

        input_margin_x = self.explorer._scaled(4)
        input_margin_y = self.explorer._scaled(1)

        self.rename_input = QLineEdit(self)
        self.rename_input.setGeometry(
            self.name_label.x() + input_margin_x,
            self.name_label.y() + input_margin_y,
            self.name_label.width() - (input_margin_x * 2),
            self.name_label.height() - (input_margin_y * 2)
        )
        self.rename_input.setAlignment(Qt.AlignCenter)
        self.rename_input.setText(self.item_name)
        self.rename_input.hide()
        self.rename_input.returnPressed.connect(self.commit_rename)

        self._apply_name_styles(False)

    def _apply_name_styles(self, selected):
        if selected:
            font_weight = "700"
        else:
            font_weight = "600"
        self.icon_panel.setStyleSheet("background-color: transparent; border: none;")

        self.name_label.setStyleSheet(f"""
            color: white;
            font-family: bahnschrift;
            font-size: {self.explorer._scaled(10)}px;
            font-weight: {font_weight};
            background-color: transparent;
        """)

        self.rename_input.setStyleSheet(f"""
            color: white;
            font-family: bahnschrift;
            font-size: {self.explorer._scaled(10)}px;
            font-weight: 700;
            background-color: rgba(8, 55, 180, 200);
            border: 1px solid rgba(157, 210, 255, 110);
            border-radius: {self.explorer._scaled(10)}px;
            padding-left: 8px;
            padding-right: 8px;
            selection-background-color: rgba(157, 210, 255, 120);
        """)

    def update_selection_style(self, selected):
        if selected:
            self.setStyleSheet(f"""
                background-color: rgba(157, 210, 255, 80);
                border: none;
                border-radius: 0px;
            """)
        else:
            self.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: none;")

        self._apply_name_styles(selected)

    def mousePressEvent(self, event):
        if self.is_renaming:
            return

        self.explorer.select_item(self.index)

        if event.button() == Qt.RightButton:
            self.explorer.open_context_menu(event.globalPosition().toPoint(), self.index)

    def mouseDoubleClickEvent(self, event):
        if self.is_renaming:
            return

        if event.button() == Qt.LeftButton:
            self.explorer.open_item(self.index)

    def start_rename(self):
        self.is_renaming = True
        self.name_label.hide()
        self.rename_input.setText(self.item_name)
        self.rename_input.show()
        self.rename_input.setFocus()
        self.rename_input.selectAll()

    def cancel_rename(self):
        self.is_renaming = False
        self.rename_input.hide()
        self.name_label.show()

    def commit_rename(self):
        new_name = self.rename_input.text().strip()

        if not new_name:
            self.explorer.show_error("Name can't be empty.")
            return

        if not self.explorer.logic.rename_item(self.item_path, new_name):
            self.explorer.show_error("Rename failed. The name may already exist or be invalid.")
            return

        self.is_renaming = False
        self.explorer.selected_path = self.item_path.parent / new_name
        self.explorer.load_directory()


class FileExplorerUIMixin:
    def add_hitbox(self, index, item_path, item_name, file_type, x, y, w, h):
        hitbox = FileItemHitbox(self, index, item_path, item_name, file_type, x, y, w, h)
        self.item_hitboxes.append(hitbox)
        return hitbox

    def clear_file_area(self):
        self.item_hitboxes = []
        for child in self.file_area.children():
            if isinstance(child, QWidget):
                child.deleteLater()

    def update_selection_styles(self):
        for hitbox in self.item_hitboxes:
            hitbox.update_selection_style(
                self.selected_path is not None and hitbox.item_path == self.selected_path
            )
        self.update_bottom_bar()

    def _setup_window(self):
        self.resize(WIDTH, HEIGHT)
        self.setMinimumSize(840, 640)
        self.setWindowTitle("LOTON File Explorer")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def _setup_ui(self):
        self.root = QWidget(self)
        self.root.setStyleSheet("""
            QWidget {
                background-color: #18039E;
                border-radius: 10px;
            }
        """)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self.root)

        self.main_layout = QVBoxLayout(self.root)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("""
            background-color: #002bbd;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        """)
        title_layout = QGridLayout(self.title_bar)
        title_layout.setContentsMargins(8, 0, 8, 0)

        title = QLabel("LOTON File Explorer")
        title.setStyleSheet("color: white; font-size: 18px;")
        self.main_layout.addWidget(self.title_bar)

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
        title_layout.addWidget(btn_close, 0, 2)
        title_layout.setColumnStretch(0, 1)

        self.address_bar = QWidget()
        self.address_bar.setFixedHeight(36)
        self.address_bar.setStyleSheet("background-color: #0022ff;")
        self.main_layout.addWidget(self.address_bar)

        self.address_layout = QHBoxLayout(self.address_bar)
        self.address_layout.setContentsMargins(8, 0, 8, 0)

        self.path_label = QLabel()
        self.path_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-family: bahnschrift;
        """)
        self.address_layout.addWidget(self.path_label)

        self.back_button = QPushButton("<")
        self.forward_button = QPushButton(">")
        for button in (self.back_button, self.forward_button):
            button.setFixedSize(28, 24)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #0084ff;
                    color: white;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #ff4444;
                }
            """)

        self.back_button.clicked.connect(self.history_back)
        self.forward_button.clicked.connect(self.history_forward)
        self.address_layout.addWidget(self.back_button)
        self.address_layout.addWidget(self.forward_button)

        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.main_layout.addWidget(self.content_widget)

        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(180)
        self.sidebar.setStyleSheet("""
            background-color: #0223aa;
            border-bottom-left-radius: 16px;
        """)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(10, 12, 10, 12)
        self.sidebar_layout.setSpacing(6)

        self.sidebar_header = QLabel("Quick Access")
        self.sidebar_header.setStyleSheet("""
            color: rgba(255, 255, 255, 160);
            font-family: bahnschrift;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            padding-left: 8px;
        """)
        self.sidebar_layout.addWidget(self.sidebar_header)

        self.sidebar_divider = QFrame(self.sidebar)
        self.sidebar_divider.setFixedHeight(1)
        self.sidebar_divider.setStyleSheet("background-color: rgba(255, 255, 255, 50); border: none;")
        self.sidebar_layout.addWidget(self.sidebar_divider)
        self.content_layout.addWidget(self.sidebar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea { background: #003eff; }
            QScrollBar:vertical {
                background: #002bbd;
                width: 12px;
                margin: 4px 0px 4px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #6fa8ff;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        self.file_area = QWidget()
        self.file_area.setStyleSheet("background-color: #003eff;")
        self.file_area.setMinimumSize(0, 0)
        self.file_area.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_area.customContextMenuRequested.connect(self.handle_right_click)
        self.file_area.mousePressEvent = self.handle_file_area_mouse_press
        self.scroll_area.setWidget(self.file_area)
        self.content_layout.addWidget(self.scroll_area)

        self.bottom_bar = QWidget()
        self.bottom_bar.setFixedHeight(42)
        self.bottom_bar.setStyleSheet("""
            background-color: #0d00c2;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        self.bottom_bar_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(12, 0, 12, 0)
        self.bottom_bar_layout.setSpacing(10)

        self.bottom_left_label = QLabel("0 item(s)")
        self.bottom_center_label = QLabel("")
        self.bottom_right_label = QLabel("No item selected")

        for label in (self.bottom_left_label, self.bottom_center_label, self.bottom_right_label):
            label.setStyleSheet("""
                color: white;
                font-family: bahnschrift;
                font-size: 12px;
                background: transparent;
                border: none;
            """)
            label.setAlignment(Qt.AlignVCenter)

        self.bottom_center_label.setStyleSheet("""
            color: rgba(255, 255, 255, 190);
            font-family: bahnschrift;
            font-size: 12px;
            background: transparent;
            border: none;
        """)
        self.bottom_right_label.setStyleSheet("""
            color: #9dd2ff;
            font-family: bahnschrift;
            font-size: 12px;
            font-weight: 700;
            background: transparent;
            border: none;
        """)

        self.bottom_bar_layout.addWidget(self.bottom_left_label, 0)
        self.bottom_bar_layout.addWidget(self.bottom_center_label, 1)
        self.bottom_bar_layout.addSpacing(1)
        self.bottom_bar_layout.addWidget(self.bottom_right_label, 10)
        self.main_layout.addWidget(self.bottom_bar)

        self.resize_handle = QWidget(self.root)
        self.resize_handle.setFixedSize(18, 18)
        self.resize_handle.setStyleSheet("""
            background-color: #6fa8ff;
            border-radius: 6px;
        """)
        self.resize_handle.setCursor(Qt.SizeFDiagCursor)

        self.custom_popup = QFrame(self.root)
        self.custom_popup.setFixedSize(self._scaled(220), self._scaled(120))
        self.custom_popup.setStyleSheet("""
            background-color: #001f8f;
            border: 2px solid #8ac5ff;
            border-radius: 12px;
        """)
        self.custom_popup.hide()

        popup_layout = QVBoxLayout(self.custom_popup)
        popup_layout.setContentsMargins(12, 12, 12, 12)
        popup_layout.setSpacing(10)

        self.popup_message = QLabel(self.custom_popup)
        self.popup_message.setAlignment(Qt.AlignCenter)
        self.popup_message.setWordWrap(True)
        self.popup_message.setStyleSheet("""
            color: white;
            font-family: bahnschrift;
            font-size: 13px;
            background: transparent;
            border: none;
        """)
        popup_layout.addWidget(self.popup_message)

        popup_buttons = QHBoxLayout()
        popup_buttons.setSpacing(8)
        popup_layout.addLayout(popup_buttons)

        self.popup_confirm_button = QPushButton("OK", self.custom_popup)
        self.popup_cancel_button = QPushButton("Cancel", self.custom_popup)
        for button in (self.popup_confirm_button, self.popup_cancel_button):
            button.setFixedHeight(self._scaled(22))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #1492ff;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 4px 10px;
                    font-family: bahnschrift;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #39a6ff;
                }
            """)

        self.popup_confirm_button.clicked.connect(self.confirm_popup)
        self.popup_cancel_button.clicked.connect(self.hide_custom_popup)
        popup_buttons.addWidget(self.popup_confirm_button)
        popup_buttons.addWidget(self.popup_cancel_button)

        self.update_layout()
        Theme_Manager.install_theme_sync()

    def update_layout(self):
        sidebar_width = max(self._scaled(120), min(self._scaled(180), self.width() // 4))
        self.sidebar.setFixedWidth(sidebar_width)

        self.root.setGeometry(0, 0, self.width(), self.height())
        self.resize_handle.move(
            self.width() - self.resize_handle.width() - 6,
            self.height() - self.resize_handle.height() - 6
        )

        if self.custom_popup is not None:
            self.custom_popup.move(
                (self.root.width() - self.custom_popup.width()) // 2,
                (self.root.height() - self.custom_popup.height()) // 2
            )

        self.apply_mask()

        if hasattr(self, "logic"):
            self.load_directory()

    def apply_mask(self):
        path = QPainterPath()
        path.addRoundedRect(self.rect(), RADIUS, RADIUS)
        self.setMask(path.toFillPolygon().toPolygon())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_layout()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_layout()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.resize_handle.underMouse():
                self.resizing = True
                self.dragging = False
                self.resize_start = event.globalPosition().toPoint()
                self.start_size = self.size()
                return
            if self.title_bar.underMouse():
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing:
            delta = event.globalPosition().toPoint() - self.resize_start
            new_w = max(self.minimumWidth(), self.start_size.width() + delta.x())
            new_h = max(self.minimumHeight(), self.start_size.height() + delta.y())
            self.resize(new_w, new_h)
            return

        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.dragging = False
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_C:
            self.copy_selected_item()
            return
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_X:
            self.cut_selected_item()
            return
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_V:
            self.paste_into_current_directory()
            return
        if event.key() == Qt.Key_Delete:
            self.delete_selected_item()
            return
        if event.key() == Qt.Key_F2:
            self.rename_selected_item()
            return
        if event.key() == Qt.Key_Escape:
            selected_hitbox = self.current_selected_hitbox()
            if selected_hitbox is not None and selected_hitbox.is_renaming:
                selected_hitbox.cancel_rename()
                return
            self.select_item(None)
            return

        super().keyPressEvent(event)

    def handle_file_area_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            selected_hitbox = self.current_selected_hitbox()
            if selected_hitbox is not None and selected_hitbox.is_renaming:
                selected_hitbox.cancel_rename()
            self.select_item(None)
