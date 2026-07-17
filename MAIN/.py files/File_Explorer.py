# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________

import sys

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QApplication, QMenu, QPushButton, QWidget

from File_Explorer_Logic import FileExplorerLogic
from File_Explorer_UI import FileExplorerUIMixin
from path import resource_path


class FileExplorer(FileExplorerUIMixin, QWidget):
    def contextMenuEvent(self, event):
        event.accept()

    def __init__(self):
        super().__init__()
        self.scale = 1.75
        self.drag_position = QPoint()
        self.dragging = False
        self.resizing = False
        self.custom_popup = None
        self.popup_message = None
        self.popup_confirm_button = None
        self.popup_cancel_button = None
        self.popup_confirm_callback = None

        self._setup_window()
        self._setup_ui()

        self.logic = FileExplorerLogic(resource_path("FILE EXPLORER", "This Device"))
        self.device_root = self.logic.get_current_path()
        self.history_log = []
        self.history_index = -1
        self.selected_index = None
        self.selected_path = None
        self.item_hitboxes = []
        self.sidebar_buttons = []

        self.setup_sidebar_items()
        self.load_directory()

    # Note: standalone_close was removed as it's unused

    def _scaled(self, value):
        return max(1, int(round(value * self.scale)))

    def select_item(self, index=None):
        items = self.logic.get_items()

        if index is None or index < 0 or index >= len(items):
            self.selected_index = None
            self.selected_path = None
        else:
            self.selected_index = index
            self.selected_path = items[index]["path"]

        self.update_selection_styles()

    def open_item(self, item):
        self.select_item(item)
        result = self.logic.open_item(item)

        if result == "directory":
            self.clear_file_area()
            self.load_directory()
            return

        if result == "file":
            items = self.logic.get_items()
            if item < 0 or item >= len(items):
                return

            file_type = self.file_detect_type(items[item]["name"])
            if file_type == "txt":
                self.logic.open_in_notepad(items[item]["path"])
                self.hide()

    def setup_sidebar_items(self):
        for button, _path in self.sidebar_buttons:
            button.deleteLater()
        self.sidebar_buttons = []

        pinned_items = [
            ("Home", resource_path("FILE EXPLORER", "This Device")),
            ("Desktop", resource_path("FILE EXPLORER", "This Device", "Desktop")),
            ("Documents", resource_path("FILE EXPLORER", "This Device", "Documents")),
            ("Downloads", resource_path("FILE EXPLORER", "This Device", "Downloads")),
            ("Pictures", resource_path("FILE EXPLORER", "This Device", "Pictures")),
            ("Music", resource_path("FILE EXPLORER", "This Device", "Music")),
            ("Videos", resource_path("FILE EXPLORER", "This Device", "Videos")),
            ("Local Disk", resource_path("FILE EXPLORER", "This Device", "Local Disk")),
            ("Network", resource_path("FILE EXPLORER", "This Device", "Network")),
        ]

        for label, path in pinned_items:
            button = QPushButton(label)
            button.setCursor(Qt.PointingHandCursor)
            button.setFixedHeight(self._scaled(26))
            button.setFocusPolicy(Qt.NoFocus)
            button.clicked.connect(lambda _checked=False, target=path: self.navigate_to_sidebar_path(target))
            self.sidebar_layout.addWidget(button)
            self.sidebar_buttons.append((button, path))

        self.sidebar_layout.addStretch(1)
        self.update_sidebar_styles()

    def navigate_to_sidebar_path(self, path):
        if self.logic.set_current_path(path):
            self.selected_index = None
            self.selected_path = None
            self.load_directory()

    def update_sidebar_styles(self):
        current_path = self.logic.get_current_path().replace("\\", "/")

        for button, target_path in self.sidebar_buttons:
            normalized_target = str(target_path).replace("\\", "/")
            is_active = current_path == normalized_target or current_path.startswith(normalized_target + "/")

            if is_active:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(157, 210, 255, 95);
                        color: white;
                        border: none;
                        border-left: 4px solid #ffffff;
                        text-align: left;
                        padding-left: 12px;
                        font-family: bahnschrift;
                        font-size: 13px;
                        font-weight: 700;
                        border-radius: 10px;
                    }
                    QPushButton:hover {
                        background-color: rgba(157, 210, 255, 120);
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: rgba(255, 255, 255, 220);
                        border: none;
                        text-align: left;
                        padding-left: 16px;
                        font-family: bahnschrift;
                        font-size: 13px;
                        border-radius: 10px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 28);
                        color: white;
                    }
                """)

    def current_selected_hitbox(self):
        for hitbox in self.item_hitboxes:
            if hitbox.item_path == self.selected_path:
                return hitbox
        return None

    def format_size(self, size_in_bytes):
        units = ["B", "KB", "MB", "GB"]
        size = float(size_in_bytes)

        for unit in units:
            if size < 1024 or unit == units[-1]:
                if unit == "B":
                    return f"{int(size)} {unit}"
                return f"{size:.1f} {unit}"
            size /= 1024

    def get_directory_summary(self):
        items = self.logic.get_items()
        folder_count = sum(1 for item in items if item["is_dir"])
        file_count = len(items) - folder_count
        return len(items), folder_count, file_count

    def get_selected_item_details(self):
        item = self.current_selected_item()
        if item is None:
            return "No item selected"

        item_path = item["path"]
        item_type = "Folder" if item["is_dir"] else "File"

        if item["is_dir"]:
            try:
                child_count = sum(1 for child in item_path.iterdir() if child.name != ".keep")
            except PermissionError:
                child_count = 0

            return f"Selected: {item['name']} | {item_type} | {child_count} item(s)"

        suffix = item_path.suffix.lower().lstrip(".")
        suffix_text = suffix.upper() if suffix else "File"

        try:
            file_size = self.format_size(item_path.stat().st_size)
        except OSError:
            file_size = "Unknown size"

        return f"Selected: {item['name']} | {suffix_text} | {file_size}"

    def update_bottom_bar(self):
        total_items, folder_count, file_count = self.get_directory_summary()
        self.bottom_left_label.setText(
            f"{total_items} item(s)   {folder_count} folder(s)   {file_count} file(s)"
        )

        current_path = self.logic.get_current_path().replace("\\", "/")
        marker = "This Device"
        marker_index = current_path.find(marker)
        display_path = current_path[marker_index:] if marker_index != -1 else current_path

        self.bottom_center_label.setText(display_path)
        self.bottom_right_label.setText(self.get_selected_item_details())

    def load_directory(self):
        self.update_adress_bar()
        items = self.logic.get_items()
        previous_selection = self.selected_path

        self.clear_file_area()

        spacing = self._scaled(126)
        viewport_width = self.scroll_area.viewport().width() - self._scaled(20)
        if viewport_width < self._scaled(200):
            viewport_width = 1000 - self.sidebar.width() - self._scaled(40)

        columns = max(1, viewport_width // spacing)

        for index, item in enumerate(items):
            file_type = "folder" if item["is_dir"] else "file"
            row = index // columns
            col = index % columns
            x = self._scaled(10) + col * spacing
            y = self._scaled(36) + row * spacing

            self.add_hitbox(
                index,
                item["path"],
                item["name"],
                file_type,
                x - self._scaled(12),
                y - self._scaled(10),
                spacing - self._scaled(12),
                spacing
            )

        try:
            self.file_area.setMinimumHeight(y + spacing)
        except UnboundLocalError:
            self.file_area.setMinimumHeight(0)

        self.file_area.setMinimumWidth(viewport_width)

        current_path = self.logic.get_current_path()
        if self.history_index == -1 or self.history_log[self.history_index] != current_path:
            self.history_log = self.history_log[:self.history_index + 1]
            self.history_log.append(current_path)
            self.history_index += 1

        refreshed_items = self.logic.get_items()
        matching_index = None
        if previous_selection is not None:
            for index, item in enumerate(refreshed_items):
                if item["path"] == previous_selection:
                    matching_index = index
                    break

        self.select_item(matching_index)
        self.update_sidebar_styles()
        self.update_bottom_bar()

    def history_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.logic.set_current_path(self.history_log[self.history_index])
            self.load_directory()

    def history_forward(self):
        if self.history_index < len(self.history_log) - 1:
            self.history_index += 1
            self.logic.set_current_path(self.history_log[self.history_index])
            self.load_directory()

    def update_adress_bar(self):
        full_path = self.logic.get_current_path().replace("\\", "/")
        marker = "This Device"
        marker_index = full_path.find(marker)
        display_path = full_path[marker_index:] if marker_index != -1 else full_path
        self.path_label.setText(display_path)

    def file_detect_type(self, file_name):
        if "." not in file_name:
            return ""
        return file_name.rsplit(".", 1)[1].lower()

    def current_selected_item(self):
        if self.selected_path is None:
            return None

        for item in self.logic.get_items():
            if item["path"] == self.selected_path:
                return item

        return None

    def show_error(self, message):
        self.show_custom_popup(message, confirm_text="OK")

    def show_custom_popup(self, message, confirm_text="OK", on_confirm=None, show_cancel=False):
        self.popup_message.setText(message)
        self.popup_confirm_callback = on_confirm
        self.popup_confirm_button.setText(confirm_text)
        self.popup_cancel_button.setVisible(show_cancel)
        self.custom_popup.show()
        self.custom_popup.raise_()

    def hide_custom_popup(self):
        self.popup_confirm_callback = None
        self.custom_popup.hide()

    def confirm_popup(self):
        callback = self.popup_confirm_callback
        self.hide_custom_popup()

        if callback is not None:
            callback()

    def copy_selected_item(self):
        item = self.current_selected_item()
        if item is not None:
            self.logic.set_clipboard(item["path"], "copy")

    def cut_selected_item(self):
        item = self.current_selected_item()
        if item is not None:
            self.logic.set_clipboard(item["path"], "cut")

    def paste_into_current_directory(self):
        if not self.logic.has_clipboard_item():
            return

        if not self.logic.paste_clipboard():
            self.show_error("Paste failed.")
            return

        self.load_directory()

    def delete_selected_item(self):
        item = self.current_selected_item()
        if item is None:
            return

        def perform_delete():
            if not self.logic.delete_file_and_folder(item["path"]):
                self.show_error("Delete failed.")
                return

            self.selected_index = None
            self.selected_path = None
            self.load_directory()

        self.show_custom_popup(
            f"Delete '{item['name']}'?",
            confirm_text="Delete",
            on_confirm=perform_delete,
            show_cancel=True
        )

    def rename_selected_item(self):
        hitbox = self.current_selected_hitbox()
        if hitbox is not None:
            hitbox.start_rename()

    def open_context_menu(self, global_pos, item_index=None):
        if item_index is not None:
            self.select_item(item_index)

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #0f49ff;
                color: white;
                border: 2px solid #d2efff;
                border-radius: 14px;
                padding: 10px 8px;
                font-family: bahnschrift;
                font-size: 13px;
            }
            QMenu::item {
                padding: 9px 24px;
                margin: 3px 6px;
                border-radius: 10px;
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: #8fd9ff;
                color: #002a93;
                font-weight: 700;
            }
            QMenu::item:pressed {
                background-color: #b8ebff;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                margin: 6px 10px;
                background: rgba(255, 255, 255, 150);
            }
            QMenu::item:disabled {
                color: rgba(255, 255, 255, 150);
            }
        """)

        selected_item = self.current_selected_item()
        rename_action = delete_action = copy_action = cut_action = None

        if selected_item is not None:
            rename_action = menu.addAction("Rename")
            copy_action = menu.addAction("Copy")
            cut_action = menu.addAction("Cut")
            delete_action = menu.addAction("Delete")
            menu.addSeparator()

        paste_action = menu.addAction("Paste")
        paste_action.setEnabled(self.logic.has_clipboard_item())

        chosen_action = menu.exec(global_pos)

        if chosen_action == rename_action:
            self.rename_selected_item()
        elif chosen_action == copy_action:
            self.copy_selected_item()
        elif chosen_action == cut_action:
            self.cut_selected_item()
        elif chosen_action == delete_action:
            self.delete_selected_item()
        elif chosen_action == paste_action:
            self.paste_into_current_directory()

    def handle_right_click(self, pos):
        global_pos = self.file_area.mapToGlobal(pos)
        self.select_item(None)
        self.open_context_menu(global_pos)

    def closeEvent(self, event):
        global _if_open, _explorer_instance
        _if_open = False
        _explorer_instance = None
        super().closeEvent(event)


_explorer_instance = None
_if_open = False


def open_file_explorer():
    global _if_open, _explorer_instance

    if _explorer_instance is None:
        _explorer_instance = FileExplorer()
    elif _explorer_instance.isVisible():
        _explorer_instance.raise_()
        _explorer_instance.activateWindow()
        _if_open = True
        return

    _explorer_instance.show()
    _explorer_instance.raise_()
    _explorer_instance.activateWindow()
    _if_open = True


def close_file_explorer():
    global _if_open, _explorer_instance
    if _explorer_instance:
        _explorer_instance.close()
        print("File Explorer closed")


def file_explorer_toggle():
    global _if_open, _explorer_instance
    if _explorer_instance is None:
        _explorer_instance = FileExplorer()
    if _explorer_instance.isVisible():
        _explorer_instance.close()
        _if_open = False
    else:
        _explorer_instance.show()
        _explorer_instance.raise_()
        _explorer_instance.activateWindow()
        _if_open = True


if __name__ == "__main__":
    _if_open = True
    app = QApplication(sys.argv)
    file_explorer = FileExplorer()
    file_explorer.show()
    sys.exit(app.exec())
