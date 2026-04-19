# LOTON OS
# Copyright (c) 2026 Louis
# Licensed under the MIT License
#___________________________________________________________________________________________________________________
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea, QPushButton, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt, QTimer, QPoint
import sys

# Vars
width = 800
height = 600

class CMD(QWidget):
    def __init__(self):
        super().__init__()

        #ALL ASSETS
        self.setWindowTitle("LOTON CMD")
        self.resize(width, height)
        self.setMinimumSize(width, height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.drag_position = QPoint()

        # Root container (contains all the stuff and shit)
        self.root = QWidget(self)
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.root.setStyleSheet("""
            QWidget {
                background-color: #00003C;
                border-radius: 16px;
            }
        """)


        
        # Title bar (The bar thing at the top of the window)
        self.title_bar = QWidget(self.root)
        self.title_bar.setGeometry(0, 0, self.width(), 36)
        self.title_bar.setStyleSheet("""
            background-color: #002bbd;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        """)
        self.title_bar.installEventFilter(self)

        title_layout = QGridLayout(self.title_bar)
        title_layout.setContentsMargins(8, 0, 8, 0)

        title = QLabel("LOTON Command Prompt")
        title.setStyleSheet("color: white; font-size: 14px;")

        #Buttons
        btn_min = QPushButton("—") #defines the button
        btn_close = QPushButton("✕") #defines the button

        for btn in (btn_min, btn_close): #Actually gives the buttons drip :D
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

        btn_min.clicked.connect(self.showMinimized) #gives the button a purpose to live
        btn_close.clicked.connect(self.hide) #gives the button a purpose to live

        title_layout.addWidget(title, 0, 0)
        title_layout.addWidget(btn_min, 0, 1)
        title_layout.addWidget(btn_close, 0, 2)
        title_layout.setColumnStretch(0, 1)

        # Main layout inside root
        main_layout = QVBoxLayout(self.root)
        main_layout.setContentsMargins(0, 36, 0, 0)  # Leave space for title bar (or not)
        main_layout.setSpacing(0)

        # CMD typing variables
        self.lines = []
        self.current_line = "> "
        self.cursor_visible = True

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        main_layout.addWidget(self.scroll_area)

        
        # Output widget
        self.output_widget = QWidget()
        self.scroll_area.setWidget(self.output_widget)
        self.layout = QVBoxLayout(self.output_widget)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.output_widget.setStyleSheet("background: transparent;")
        self.output_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )



        # Display label
        self.display_label = QLabel(self.current_line)
        self.display_label.setStyleSheet("""
            font-family: 'Segoe UI';
            font-size: 16px;
            color: #fff;
            background: transparent;
        """)
        self.display_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.display_label.setWordWrap(False)
        self.display_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(self.display_label)

        self.print_banner()
        self.update_display()

        # Cursor blinking
        self.cursor_timer = QTimer()
        self.cursor_timer.timeout.connect(self.blink_cursor)
        self.cursor_timer.start(500)




    #ALL ASSETS end I think :D

    # #################################
    #important definitions I guess

    def print_banner(self):
        self.lines.append("LOTON OS [Version 1.1.0.0]")
        self.lines.append("(c) LOTON Corporation. All rights reserved.")
        self.lines.append("")


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.title_bar.underMouse():
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.title_bar.underMouse():
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.title_bar.setGeometry(0, 0, self.width(), 36)




    # #################################
    # ########## LOGIC START ##########
    # #################################

    #This shi hurts ma brain kinda

    # ---------- Methods ----------

    def CMD_clear(self):
        self.lines = []  # Clear all previous lines including responses and user inputs
    def CMD_shutdown(self):
        self.hide()  # Hides the CMD window
        self.CMD_clear()  # Clears the CMD display


    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        self.update_display()

    def update_display(self):
        full_text = "\n".join(self.lines + [self.current_line + ("|" if self.cursor_visible else " ")])
        self.display_label.setText(full_text)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def keyPressEvent(self, event):
        text = event.text()
        key = event.key()
        modifiers = event.modifiers()

        # Ctrl + Backspace
        if key == Qt.Key_Backspace and modifiers == Qt.ControlModifier:
            parts = self.current_line[2:].split()  # remove "> "
            if parts:
                parts = parts[:-1]
                self.current_line = "> " + " ".join(parts)
            else:
                self.current_line = "> "

        # Normal Backspace
        elif key == Qt.Key_Backspace:
            if len(self.current_line) > 2:
                self.current_line = self.current_line[:-1]

        # Enter
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            command = self.current_line[2:]  # skip "> "
            self.lines.append(self.current_line)
            self.user_input_check(command)
            self.current_line = "> "

        # Printable characters
        elif text.isprintable() and text != "":
            self.current_line += text

        self.update_display()


    #all def stuff for the logic of the CMD goes here ye

    def user_input_check(self, command): #This runs everytime enter is pressed (so this do be getting reused :fire:)
        #All the def stuff can go here ye
        #There will be a lotta if statements here but prob fine hopefully :D
        #Example:
        #__________________________________________________________________
        #if command.lower() == "hello":
        #    response = "Hello there! How can I assist you today?"
        #else:
        #    response = f"Command not recognized: {command}"
        #self.lines.append(response)
        #__________________________________________________________________
        #Now time for actual commands :D
        #I'ma make a few basic ones first and then add more later :P
        if command.lower() == "/help":
            response = \
            """Available commands: /help; /echo [text], /clear; /about; /exit; /time (0 h time zone); /date; /open calculator; /open notepad; /shutdown""" #a total of 10 commands boys :fire:
            self.lines.append(response) #prints (aka shows) the system response (on screen)

        elif command.lower().startswith("/echo "):
            response = command[6:]  # Get text after "/echo "
            self.lines.append(response) #prints the echoed text (again js like the above /help command thing :D)

        elif command.lower() == "/clear":
            self.lines = []  # Clear all previous lines including responses and user inputs and shit
        
        elif command.lower() == "/about":
            response = "LOTON command prompt v1.0. Created by LOTON's (only) developer."
            self.lines.append(response) #prints the about info
            response = "LOTON Corporation © , All Rights Reserved."
            self.lines.append(response)  # prints the about info
            response = "Found date: 2025"
            self.lines.append(response)  # prints the about info
            response = "Current version: 1.1.0.0"
            self.lines.append(response)  # prints the about info
        elif command.lower() == "/exit":
            self.hide()  # Hides the CMD window

        elif command.lower() == "/time":
            from datetime import datetime #only import stuff when needed (or not if u want when u edit this since LOTON is open source after all :D)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            response = f"Current Time (UTC+0): {current_time}" #stores the time thing
            self.lines.append(response)  # prints the current time aka response

        elif command.lower() == "/date":
            from datetime import datetime
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            response = f"Current Date: {current_date}"
            self.lines.append(response)  # prints the current date aka response

        elif command.lower() == "/open calculator":
            import Calculator  #import the calculator file when needed
            Calculator.turn_on_calculator() #the turn on def thing in calculator.py
            response = "Calculator opened."
            self.lines.append(response)  # prints the response

        elif command.lower() == "/open notepad":
            import Notepad  #import the notepad file when needed
            Notepad.notepad_activate() #the activate def thing in notepad.py
            response = "Notepad opened."
            self.lines.append(response)  # prints the response
        #we need more commands :D

        elif command.lower() == "/shutdown":
            response = "Shutting down LOTON CMD..."
            self.lines.append(response)  # prints the response
            QTimer.singleShot(2000, self.CMD_shutdown)  # Wait 2 seconds before hiding the window and clearing everything

        else:
            response = f"Command not recognized: {command}"
            self.lines.append(response)  # prints unrecognized command message


    # ###############################
    # ########## LOGIC END ##########
    # ###############################

_cmd_instance = None

    #Turn on and off definitions
def cmd_activate():
    """Show and focus the global CMD instance."""
    global _cmd_instance
    if QApplication.instance() is None:
        QApplication(sys.argv)
    if _cmd_instance is None:
        _cmd_instance = CMD()
    _cmd_instance.show()
    _cmd_instance.raise_()
    _cmd_instance.activateWindow()

def cmd_deactivate():
    """Hide the CMD window if present."""
    if _cmd_instance:
        _cmd_instance.hide()

def turn_off_cmd():
    """Hide the CMD window if present."""
    sys.exit()


#After IDK how many lines of code, it finally runs right under here phew :P
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
QScrollBar:vertical {
    background: transparent;
    width: 24px;
    margin: 12px 6px 12px 6px;
}
QScrollBar::handle:vertical {
    background: rgba(255,255,255,0.22);
    min-height: 48px;
    border-radius: 12px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(255,255,255,0.36);
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
    height: 0;
}

QScrollBar:horizontal {
    background: transparent;
    height: 24px;
    margin: 6px 12px 6px 12px;
}
QScrollBar::handle:horizontal {
    background: rgba(255,255,255,0.22);
    min-width: 48px;
    border-radius: 12px;
}
QScrollBar::handle:horizontal:hover {
    background: rgba(255,255,255,0.36);
}
""")
    window = CMD()
    window.show()
    sys.exit(app.exec())