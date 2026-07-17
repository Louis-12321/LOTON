# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QPushButton, QLineEdit
)
from path import resource_path
from PySide6.QtCore import Qt
import sys
from pathlib import Path

WIDTH = 360
HEIGHT = 220

window_title = "File Name"
content = "Save as:"

class Popup(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent

        #region INIT

        # Window setup
        self.setWindowTitle("LOTON Popup")
        self.resize(WIDTH, HEIGHT)

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)

        #endregion

        # Root container
        self.root = QWidget(self)
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.root.setStyleSheet("""
            QWidget {
                background-color: #4266f5;
                border-radius: 16px;
            }
        """)

        #region GUI

        #================================
        #           TITLE BAR
        #================================
        self.title_bar = QWidget(self.root)
        self.title_bar.setGeometry(0, 0, self.width(), 36)
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("""
            background-color: #002bbd;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        """)

        title_layout = QGridLayout(self.title_bar)
        title_layout.setContentsMargins(8, 0, 8, 0)

        self.title = QLabel(window_title)
        self.title.setStyleSheet("color: white; font-size: 18px;")

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

        btn_close.clicked.connect(self.close)

        title_layout.addWidget(self.title, 0, 0)
        title_layout.addWidget(btn_close, 0, 2)
        title_layout.setColumnStretch(0, 1)

        #===============================
        #           MESSAGE
        #===============================
        self.message = QLabel(content, self.root)
        self.message.setGeometry(3, 37, self.width(), self.height() - 36)
        self.message.setAlignment(Qt.AlignLeft)
        self.message.setWordWrap(True)
        self.message.setStyleSheet("color: white; font-size: 20px;")

        #==============================
        #       TYPE ZONE
        #==============================
        self.typezone = QLineEdit(self.root)
        self.typezone.setGeometry(10, 100, 300, 50)
        self.typezone.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: #0380fc;
                border: 2px solid white;
                font-size: 25px;
                font-family: Bahnschrift;
                padding: 12px;
                border-radius: 10px;
            }
        """)
        self.typezone.setPlaceholderText("Name...")
        self.typezone.returnPressed.connect(self.get_file_name)

        #==============================
        #           BUTTONS
        #==============================
        btn_yes = QPushButton("Save")
        btn_cancel = QPushButton("Cancel")

        for btn in (btn_yes, btn_cancel):
            btn.setFixedSize(80, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0040ff;
                    color: white;
                    border: 2px solid white;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #ff4444;
                }
            """)
            btn.setFocusPolicy(Qt.NoFocus)

        btn_yes.setParent(self.root)
        btn_cancel.setParent(self.root)

        btn_yes.move(80, 175)
        btn_cancel.move(190, 175)

        btn_cancel.clicked.connect(self.close)
        btn_yes.clicked.connect(self.get_file_name)

    #region DEFINITIONS

    def hide_all(self):
        self.hide()

    def get_file_name(self):
        query = self.typezone.text().strip()

        if not query:
            return

        if not query.endswith(".txt"):
            query += ".txt"

        if self.parent_window:
            # update title
            self.parent_window.setWindowTitle(f"LOTON Notepad - {query}")
            self.parent_window.title.setText(f"LOTON Notepad - {query}")

            # folder path
            save_folder = resource_path(
                "FILE EXPLORER",
                "This Device",
                "Documents",
                "Saved Files"
            )
            

            # create folder if missing
            Path(save_folder).mkdir(parents=True, exist_ok=True)

            # final file path
            file_path = Path(save_folder) / query

            # get notepad text
            content = self.parent_window.text_area.toPlainText()

            # write file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print("Saved:", file_path)

        self.close()

#run standalone
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Popup()
    window.show()
    sys.exit(app.exec())
