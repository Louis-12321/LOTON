# LOTON OS
# Copyright (c) 2026 Louis
# Licensed under the MIT License
#___________________________________________________________________________________________________________________

#region IMPORTS

from PySide6.QtWidgets import (
    QApplication, QLineEdit, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QHBoxLayout, QPushButton,
    QScrollArea, QFrame,
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QCursor, QPixmap, QPainterPath, QFontMetrics
import sys
from File_Explorer_Logic import FileExplorerLogic
from path import asset_path, resource_path

WIDTH = 1000
HEIGHT = 700
RADIUS = 16

#endregion

class FileExplorer(QWidget):
    def contextMenuEvent(self, event):
        event.accept()
    def __init__(self):
        super().__init__()
        self.scale = 1.75
        self.drag_position = QPoint()
        self.resizing = False
        self._setup_window()
        self._setup_ui()
        DEVICE_PATH = resource_path("FILE EXPLORER", "This Device")
        self.logic = FileExplorerLogic(
            DEVICE_PATH
        )
        self.history_log = []
        self.history_index = -1
        self.load_directory()

    def standalone_close():
        if _explorer_instance:
            _explorer_instance.close()

    #============================
    #           MAIN
    #============================
    #region MAIN

    def _scaled(self, value):
        return max(1, int(round(value * self.scale)))

    def show_tab(self, text, file, path, x, y, w, h):
        file_type = file.lower()

        if file_type == "folder":
            source_path = asset_path("Real Assets", "File Explorer", "Folder icon.png")
        elif file_type == "file":
            source_path = asset_path("Real Assets", "File Explorer", "File icon.png")
        else:
            return

        # ICON
        icon = QLabel(self.file_area)
        icon.setGeometry(x, y, w, h)

        pixmap = QPixmap(source_path)
        icon.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.setAlignment(Qt.AlignCenter)
        icon.show()

        # TEXT SETUP
        text_gap = self._scaled(10)
        text_height = self._scaled(40)
        font_size = self._scaled(10)
        text_width = self._scaled(104)

        fm = QFontMetrics(self.font())

        if fm.horizontalAdvance(text) > text_width - self._scaled(10):
            trimmed_text = fm.elidedText(text, Qt.ElideRight, text_width - self._scaled(10))
        else:
            trimmed_text = text

        # LABEL
        file_name = QLineEdit(self.file_area)
        file_name.setContextMenuPolicy(Qt.NoContextMenu)
        file_name.setCursor(Qt.ArrowCursor)
        file_name.setText(trimmed_text)
        file_name.setToolTip(text)
        file_name.setAlignment(Qt.AlignCenter)
        

        file_name.setStyleSheet(f"""
            color: white;
            font-family: bahnschrift;
            font-size: {font_size}px;
            border: none;
            background: transparent;
        """)

        file_name.setFixedSize(text_width, text_height)
        file_name.setGeometry(x - self._scaled(20), y + h + text_gap, text_width, text_height)
        file_name.setReadOnly(True)

        # EVENTS
        """
        def enable_edit(event):
            file_name.setReadOnly(False)
            file_name.setFocus()

        file_name.mouseDoubleClickEvent = enable_edit

        file_name.returnPressed.connect(
            lambda: self.logic.finish_rename(
                file_name.property("full_path"),
                file_name
            )
        )
        """

        file_name.show()
        if file.lower() == "folder":
            foi_path = asset_path("Real Assets", "File Explorer", "Folder icon.png")
        elif file.lower() == "file":
            fi_path = asset_path("Real Assets", "File Explorer", "File icon.png")
        else:
            return

        icon = QLabel(self.file_area)
        icon.setGeometry(x, y, w, h)

        source_path = foi_path if file.lower() == "folder" else fi_path
        pixmap = QPixmap(source_path)
        scaled_pixmap = pixmap.scaled(
            w,
            h,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        icon.setPixmap(scaled_pixmap)
        icon.setAlignment(Qt.AlignCenter)
        icon.show()

        text_gap = self._scaled(10)
        text_height = self._scaled(40)
        font_size = self._scaled(10)

        # Keep names readable by giving name label the same width as spacing.
        text_width = self._scaled(104)  # icon width 64 plus padding
        fm = QFontMetrics(self.font())  # or any temp font
        trimmed_text = text

        if fm.horizontalAdvance(text) > text_width - self._scaled(10):
            trimmed_text = fm.elidedText(text, Qt.ElideRight, text_width - self._scaled(10))


        file_name = QLineEdit(self.file_area)
        file_name.setText(trimmed_text)
        file_name.setAlignment(Qt.AlignCenter)
        file_name.setStyleSheet(f"""
            color: white;
            font-family: bahnschrift;
            font-size: {font_size}px;
            border: none;
            background: transparent;
        """)
        file_name.setFixedWidth(text_width)
        file_name.setFixedHeight(text_height)
        file_name.setGeometry(x - self._scaled(20), y + h + text_gap, text_width, text_height)
        file_name.setReadOnly(True)

        """
        def enable_edit(event):
            file_name.setReadOnly(False)
            file_name.setFocus()

        file_name.mouseDoubleClickEvent = enable_edit

        file_name.returnPressed.connect(
        lambda: self.logic.finish_rename(
            file_name.property("full_path"),
            file_name
        )
        )
        """
        if fm.horizontalAdvance(text) > text_width - self._scaled(10):
            trimmed_text = fm.elidedText(text, Qt.ElideRight, text_width - self._scaled(10))

        file_name.setText(trimmed_text)
        file_name.setToolTip(text)
        file_name.setAlignment(Qt.AlignCenter)
        file_name.setStyleSheet(f"color: white; font-family: bahnschrift; font-size: {font_size}px;")

        file_name.show()

    def add_hitbox(self, x, y, w, h, callback): #The hitbox for opening files/folders
        hitbox = QWidget(self.file_area)
        hitbox.setGeometry(x, y, w, h)
        hitbox.setStyleSheet("background-color: rgba(0, 0, 0, 0);") 
        hitbox.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        hitbox.mousePressEvent = lambda event: callback()
        hitbox.show()

        #remove files

    def clear_file_area(self):
        for child in self.file_area.children():
            if isinstance(child, QWidget):
                child.deleteLater()

    def open_item(self, item):
        result = self.logic.open_item(item)

        if result == "directory":
            self.clear_file_area()
            self.load_directory()
        elif result == "file":
            file_type = self.file_detect_type(self.logic.get_items()[item]["name"])
            if file_type == "txt":
                self.logic.open_in_notepad(self.logic.get_items()[item]["path"])
                self.hide()

    def load_directory(self):
        self.update_adress_bar()
        items = self.logic.get_items()

        self.clear_file_area()

        icon_size = self._scaled(64)
        spacing = self._scaled(120)

        viewport_width = self.scroll_area.viewport().width() - self._scaled(20)
        if viewport_width < self._scaled(200):
            viewport_width = WIDTH - self.sidebar.width() - self._scaled(40)

        columns = max(1, viewport_width // spacing)

        for i, item in enumerate(items):
            if item["is_dir"]:
                filetype = "folder"
            else:
                filetype = "file"

            row = i // columns
            col = i % columns
            x = self._scaled(10) + col * spacing
            y = self._scaled(40) + row * spacing

            self.show_tab(
                item["name"],
                filetype,
                item["path"],
                x,
                y,
                icon_size,
                icon_size
            )

            self.add_hitbox(
                x,
                y - 30,
                spacing - 100,
                spacing - 30,
                lambda idx=i: self.open_item(idx)
            )

            x += spacing

        # Make sure the scroll area can scroll vertical content
        try:
            self.file_area.setMinimumHeight(y + spacing)
        except UnboundLocalError:
            self.file_area.setMinimumHeight(0)
        self.file_area.setMinimumWidth(viewport_width)

        #History adding
        current_path = self.logic.get_current_path()
        if self.history_index == -1 or self.history_log[self.history_index] != current_path:
            self.history_log = self.history_log[:self.history_index + 1]
            self.history_log.append(current_path)
            self.history_index += 1

    def history_back(self): #A history key/button that returns you to the previous directory
        if self.history_index > 0:
            self.history_index -= 1
            previous_path = self.history_log[self.history_index]

            self.logic.set_current_path(previous_path)
            self.load_directory()
            print(f"History back: {previous_path}")

    def history_forward(self): #A history key/button that returns you to the next directory if you went back
        if self.history_index < len(self.history_log) - 1:
            self.history_index += 1
            next_path = self.history_log[self.history_index]

            self.logic.set_current_path(next_path)
            self.load_directory()
            print(f"History forward: {next_path}")

    def update_adress_bar(self):
        full_path = self.logic.get_current_path().replace("\\", "/")
        marker = "This Device"
        marker_index = full_path.find(marker)

        if marker_index != -1:
            display_path = full_path[marker_index:]
        else:
            display_path = full_path

        self.path_label.setText(display_path)

    def file_detect_type(self, file_name):
        if "." in file_name:
            print(file_name.rsplit(".", 1)[1].lower())
        return file_name.rsplit(".", 1)[1].lower()

    def handle_right_click(self, pos):
        self.menu_is_open = False

        if self.menu_is_open:
            self.right_mouse_menu.hide()
            self.menu_is_open = False
            return
        else:
            pos = self.mapFromGlobal(QCursor.pos())
            self.right_mouse_menu.move(pos)
            self.right_mouse_menu.show()
            self.menu_is_open = True

    #region WINDOW

    def _setup_window(self):
        self.resize(WIDTH, HEIGHT)
        self.setMinimumSize(640, 420)
        self.setWindowTitle("LOTON File Explorer")

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
    
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
        #endregion

        #region GUI

        # =========================
        # TITLE BAR
        # =========================
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

        title_layout.addWidget(title, 0, 0)

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

        standalone = False

        btn_min.clicked.connect(self.showMinimized)
        if standalone == False:
            btn_close.clicked.connect(self.close)
        else:
            btn_close.clicked.connect(close_file_explorer)

        title_layout.addWidget(title, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        title_layout.addWidget(btn_min, 0, 1)
        title_layout.addWidget(btn_close, 0, 2)
        title_layout.setColumnStretch(0, 1)

        # =========================
        #      ADDRESS BAR
        # =========================
        self.address_bar = QWidget()
        self.address_bar.setFixedHeight(36)
        self.address_bar.setStyleSheet("""
            background-color: #0022ff;
        """)
        self.main_layout.addWidget(self.address_bar)
        self.address_layout = QHBoxLayout(self.address_bar)
        self.address_layout.setContentsMargins(8, 0, 8, 0)



        self.path_label = QLabel()
        self.path_label.setStyleSheet("""
        color: white; 
        font-size:20px;
        font-family: bahnschrift;
        """)
        self.address_layout.addWidget(self.path_label)

        #Speaking of address bar, I'ma just ruin the name by adding a back to previous directory button :D
        self.back_button = QPushButton("<")
        self.back_button.setFixedSize(28, 24)
        self.back_button.setStyleSheet("""
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
        self.address_layout.addWidget(self.back_button)

        self.forward_button = QPushButton(">")
        self.forward_button.setFixedSize(28, 24)
        self.forward_button.setStyleSheet("""
            QPushButton {
                background-color: #0084ff;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)
        self.forward_button.clicked.connect(self.history_forward)
        self.address_layout.addWidget(self.forward_button)

        # =========================
        #      CONTENT AREA
        # =========================
        self.content_widget = QWidget()
        content_layout = QHBoxLayout(self.content_widget)
        self.content_layout = content_layout
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.main_layout.addWidget(self.content_widget)

        # ========================
        #         SIDEBAR
        # ========================
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(100)
        self.sidebar.setStyleSheet("""
            background-color: #002bbd;
        """)

        content_layout.addWidget(self.sidebar)

        #=========================
        #       BOTTOMBAR
        #=========================
        self.bottom_bar = QWidget()
        self.bottom_bar.setFixedHeight(36)
        self.bottom_bar.setStyleSheet("""
            background-color: #0d00c2;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        self.main_layout.addWidget(self.bottom_bar)

        # ===========================
        # MAIN FILE AREA (SCROLLABLE)
        # ===========================
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        # Customize scroll bar style to avoid default ugly appearance.
        self.scroll_area.setStyleSheet('''
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
        ''')

        self.file_area = QWidget()
        self.file_area.setStyleSheet("""
            background-color: #003eff;
        """)
        self.file_area.setMinimumSize(0, 0)

        self.scroll_area.setWidget(self.file_area)
        content_layout.addWidget(self.scroll_area)
        
        self.resize_handle = QWidget(self.root)
        self.resize_handle.setFixedSize(18, 18)
        self.resize_handle.setStyleSheet("""
            background-color: #6fa8ff;
            border-radius: 6px;
        """)
        self.resize_handle.setCursor(Qt.SizeFDiagCursor)

        self.update_layout()

        #============================
        #     RIGHT CLICK MENU
        #============================

        """self.right_mouse_menu = QWidget(self)
        self.right_mouse_menu.setStyleSheet("""
            #background-color: #002bbd;
            #border: 1px solid #000;
            #border-radius: 6px;
        """)
        self.right_mouse_menu_layout = QVBoxLayout(self.right_mouse_menu)
        self.right_mouse_menu.hide()
        self.file_area.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_area.customContextMenuRequested.connect(self.handle_right_click)
        """
        #endregion

    #endregion

    #region RESIZING

    def update_layout(self):
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.resize_handle.move(
            self.width() - self.resize_handle.width() - 6,
            self.height() - self.resize_handle.height() - 6
        )
        self.apply_mask()

        # Reflow icons when the window size changes
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
                self.resize_start = event.globalPosition().toPoint()
                self.start_size = self.size()
                return
            if self.title_bar.underMouse():
                self.drag_position = (
                    event.globalPosition().toPoint()
                    - self.frameGeometry().topLeft()
                )

    def mouseMoveEvent(self, event):
        if self.resizing:
            delta = event.globalPosition().toPoint() - self.resize_start
            new_w = max(self.minimumWidth(), self.start_size.width() + delta.x())
            new_h = max(self.minimumHeight(), self.start_size.height() + delta.y())
            self.resize(new_w, new_h)
            return

        if event.buttons() == Qt.LeftButton and self.title_bar.underMouse():
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, event):
        
        self.resizing = False
    #endregion

    def closeEvent(self, event):
        global _if_open, _explorer_instance
        _if_open = False
        _explorer_instance = None
        super().closeEvent(event)
        
#============================
#   LINKING TO MAIN FILE
#============================

#region LINKING

#these defs are for linking the main file to the main LOTON file so that we can open the File Explorer
#from the main file without having to do FileExplorer().show() in the main file
#AKA how real OS works or smthing
#So yeah
#I've done this thing like ummm 3 times so I've got the hang of it :D

_explorer_instance = None
_if_open = False

def open_file_explorer():
    global _if_open
    global _explorer_instance

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
    global _if_open
    global _explorer_instance
    if _explorer_instance:
        _explorer_instance.close()
        print("File Explorer closed")

def hide_file_explorer():
    global _if_open
    global _explorer_instance
    if _explorer_instance:
        _explorer_instance.hide()
        _if_open = False

def cold_start_file_explorer():
    global _explorer_instance
    global file_explorer
    
    if _explorer_instance is None:
        file_explorer = FileExplorer()
        hide_file_explorer()
    else:
        return



#endregion

# =============================
# STANDALONE TESTING
# =============================
if __name__ == "__main__":
    _if_open = True
    _standalone = True
    app = QApplication(sys.argv)
    file_explorer = FileExplorer()
    file_explorer.show()
    sys.exit(app.exec())
#Alright -5 braincells after writing this
