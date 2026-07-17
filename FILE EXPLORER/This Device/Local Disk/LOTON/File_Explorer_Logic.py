# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________

import shutil
from pathlib import Path
from Notepad import notepad_activate

class FileExplorerLogic:

    # region LOGIC

    def __init__(self, start_path):
        self.current_dir = Path(start_path)
        self.clipboard_path = None
        self.clipboard_mode = None

    def get_items(self):
        items = []

        try:
            for item in self.current_dir.iterdir():
                if item.name == ".keep":
                    continue

                items.append({
                    "name": item.name,
                    "path": item,
                    "is_dir": item.is_dir()
                })
        except PermissionError:
            return []

        return self.sort_items(items)

    def open_item(self, index):
        #double click
        if index is None:
            return None
        items = self.get_items()

        if index < 0 or index >= len(items):
            return None

        selected = items[index]["path"]

        if selected.is_dir():
            self.current_dir = selected
            return "directory"
        
    
        return "file"

    def go_back(self):
        parent = self.current_dir.parent

        if parent != self.current_dir:
            self.current_dir = parent
            return True

        return False

    def get_current_path(self):
        return str(self.current_dir)
    
    def set_current_path(self, path):
        new_path = Path(path)

        if new_path.is_dir():
            self.current_dir = new_path
            return True

        return False
    
    #Sorting
    def sort_items(self, items, sort_by="name", ascending=True):

        if sort_by == "name":
            return sorted(
                items,
                key=lambda x: (not x["is_dir"], x["name"].lower()),
                reverse=not ascending
            )

        elif sort_by == "type":
            return sorted(
                items,
                key=lambda x: (not x["is_dir"], x["path"].suffix.lower(), x["name"].lower())
            )

        return items
    
    def open_in_notepad(self, file_path):
        notepad_activate(file_path)

    def _build_duplicate_path(self, source, destination):
        source = Path(source)
        destination = Path(destination)

        stem = source.stem if source.is_file() else source.name
        suffix = source.suffix if source.is_file() else ""
        candidate = destination / source.name

        if not candidate.exists():
            return candidate

        copy_index = 1
        while True:
            candidate_name = f"{stem} ({copy_index}){suffix}"

            candidate = destination / candidate_name
            if not candidate.exists():
                return candidate

            copy_index += 1

    def _copy_path(self, source, destination):
        source = Path(source)
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)

        dest_path = self._build_duplicate_path(source, destination)

        if source.is_dir():
            shutil.copytree(source, dest_path)
        else:
            shutil.copy2(source, dest_path)

        return dest_path

    def copy_file(self, source, destination):
        try:
            self._copy_path(source, destination)
            return True

        except Exception as e:
            print(f"Error copying file: {e}")
            return False
        
        #:D
    
    def cut_file(self, source, destination):
        try:
            source = Path(source)
            destination = Path(destination)
            destination.mkdir(parents=True, exist_ok=True)

            if source.parent == destination:
                return True

            dest_path = self._build_duplicate_path(source, destination)
            shutil.move(str(source), str(dest_path))

            return True

        except Exception as e:
            print(f"Error during cut operation: {e}")
            return False

    def delete_file_and_folder(self, file_path):
        try:
            file_path = Path(file_path)

            if file_path.is_dir():
                shutil.rmtree(file_path)
            elif file_path.exists():
                file_path.unlink()
            else:
                return False

            return True
        except Exception as e:
            print(f"Error deleting file/folder: {e}")
            return False

    def rename_item(self, old_path, new_name):
        try:
            old_path = Path(old_path)
            new_name = new_name.strip()

            if not new_name:
                return False

            new_path = old_path.parent / new_name

            if new_path == old_path:
                return True

            if new_path.exists():
                return False

            old_path.rename(new_path)
            print(f"Renamed to: {new_name}")
            return True

        except Exception as e:
            print(f"Error renaming file/folder: {e}")
            return False

    def finish_rename(self, old_path, file_name_widget):
        renamed = self.rename_item(old_path, file_name_widget.text())

        if renamed:
            file_name_widget.setReadOnly(True)

        return renamed

    def set_clipboard(self, source, mode):
        source = Path(source)

        if not source.exists():
            return False

        if mode not in {"copy", "cut"}:
            return False

        self.clipboard_path = source
        self.clipboard_mode = mode
        return True

    def clear_clipboard(self):
        self.clipboard_path = None
        self.clipboard_mode = None

    def has_clipboard_item(self):
        return self.clipboard_path is not None and self.clipboard_mode is not None

    def paste_clipboard(self, destination=None):
        if not self.has_clipboard_item():
            return False

        destination = Path(destination) if destination else self.current_dir
        source = Path(self.clipboard_path)

        if not source.exists():
            self.clear_clipboard()
            return False

        try:
            if self.clipboard_mode == "copy":
                self._copy_path(source, destination)
            else:
                if source.parent != destination:
                    dest_path = self._build_duplicate_path(source, destination)
                    shutil.move(str(source), str(dest_path))
                self.clear_clipboard()

            return True
        except Exception as e:
            print(f"Error pasting item: {e}")
            return False

#I think I lost like 6 of my braincells writing this