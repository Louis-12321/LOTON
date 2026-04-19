# LOTON OS
# Copyright (c) 2026 Louis
# Licensed under the MIT License
#___________________________________________________________________________________________________________________

from pathlib import Path
from Notepad import notepad_activate

class FileExplorerLogic:

    # region LOGIC

    def __init__(self, start_path):
        self.current_dir = Path(start_path)

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

        return items

    def open_item(self, index):
        #double click
        if index is None:
            return None
        items = list(self.current_dir.iterdir())

        if index < 0 or index >= len(items):
            return None

        selected = items[index]

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

    def copy_file(self, source, destination):
        try:
            source = Path(source)
            destination = Path(destination)
            destination.mkdir(parents=True, exist_ok=True)

            dest_path = destination / source.name

            if dest_path.exists():
                return False

            with open(source, 'rb') as src_file, open(dest_path, 'wb') as dst_file:
                while chunk := src_file.read(1024 * 1024):  # 1MB chunks
                    dst_file.write(chunk)

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

            dest_path = destination / source.name

            if dest_path.exists():
                return False

            # Copy first
            if not self.copy_file(source, destination):
                return False

            # Only delete if copy succeeded
            source.unlink()

            return True

        except Exception as e:
            print(f"Error during cut operation: {e}")
            return False

    def delete_file_and_folder(self, file_path):
        try:
            Path(file_path).rmdir()
            return True
        except Exception as e:
            print(f"Error deleting file/folder: {e}")
            return False

    def finish_rename(self, old_path, file_name_widget):
        try:
            old_path = Path(old_path)
            new_name = file_name_widget.text()
            new_path = old_path.parent / new_name

            if new_path.exists():
                return False

            old_path.rename(new_path)
            file_name_widget.setReadOnly(True)

            print(f"Renamed to: {new_name}")
            return True

        except Exception as e:
            print(f"Error renaming file/folder: {e}")
            return False

#I think I lost like 6 of my braincells writing this
