# LOTON OS
# Copyright (c) 2026 Louis
# Licensed under the MIT License
#___________________________________________________________________________________________________________________

#region IMPORTS
import Loading_Screen
Loading_Screen.update_loading_text("Initializing LOTON...")
import PySide6 #A timer
Loading_Screen.update_loading_text("Importing PySide6 widgets...")
#Pyside6 imports
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget
Loading_Screen.update_loading_text("Importing PySide6 graphics...")
from PySide6.QtGui import QPixmap, QMovie
Loading_Screen.update_loading_text("Importing PySide6 core...")
from PySide6.QtCore import Qt, QTimer
#System imports
Loading_Screen.update_loading_text("Importing system modules...")
import sys
from pathlib import Path
#App imports
Loading_Screen.update_loading_text("Starting LOTON...")
import Calculator
Loading_Screen.update_loading_text("Loading Command Prompt...")
import CMD
Loading_Screen.update_loading_text("Loading Notepad...")
import Notepad
Loading_Screen.update_loading_text("Loading Start Menu...")
from Start_Menu import StartMenu
Loading_Screen.update_loading_text("Loading File Explorer...")
import File_Explorer
Loading_Screen.update_loading_text("Loading login screen...")
import Login
#endregion

# Base/project paths
# Support normal source run and PyInstaller one-file/one-dir bundles
if getattr(sys, 'frozen', False):
    # when bundled by PyInstaller, resources are in _MEIPASS
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / "Assets"

def asset_path(*parts):
    return str(ASSETS_DIR.joinpath(*parts))

USING_BOOT_SPLASH = Loading_Screen.is_boot_splash_available()
SOURCE_STARTUP_DELAY_MS = 3000

#Variables
file_explorer_check = 0
calculator_check = 0
start_menu_open = 0


shutdowntextwidth = 1080
shutdowntextheight = 145
shutdowntextx = 420
shutdowntexty = 467


Loading_Screen.update_loading_text("Creating LOTON shell...")
Loton = QApplication(sys.argv)
Loading_Screen.update_loading_text("Opening login screen...")
login_window = Login.login_activate()  # Runs the login window on top of the desktop app
QTimer.singleShot(0, Loading_Screen.close_loading_screen)
# Global scrollbar stylesheet to match Notepad theme (thicker, rounded handles)
global_scrollbar_css = """
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
"""
# Apply globally
Loton.setStyleSheet(global_scrollbar_css)
# Get screen size
screen = Loton.primaryScreen()
size = screen.size()
width = size.width()
height = size.height()

# Main desktop window
desktop = QMainWindow()
desktop.setWindowTitle("Loton OS v1.2.0.0") #For alt-tab name
desktop.setGeometry(0, 0, width, height)

central = QWidget(desktop)
desktop.setCentralWidget(central)   

def on_app_opened_from_start_menu():
    global start_menu_open
    start_menu_open = 0


startup_bg = QLabel(central)
startup_bg.setGeometry(0, 0, width, height)
startup_bg.setStyleSheet("background-color: black;")
startup_bg.hide()

shutdowntext = QLabel(central)
sdt_path = asset_path("Real assets", "LOTON shut down", "Shutting Down.png")
shutdowntext.setPixmap(QPixmap(sdt_path))
shutdowntext.setGeometry(420, 451, 1080, 178)
shutdowntext.setAttribute(Qt.WA_TransparentForMouseEvents, True)
shutdowntext.hide()

#shutdown hitbox
shutdownhitbox = QPushButton(central)
shutdownhitbox.setGeometry(7, 900, 62, 62)
shutdownhitbox.setStyleSheet("""
    background-color: transparent;
    border: none;
    color: transparent;
""")
shutdownhitbox.hide()
shutdownhitbox.setCursor(Qt.PointingHandCursor)
shutdownhitbox.setAttribute(Qt.WA_TransparentForMouseEvents, False)

# --- Shutdown function ---

def kill_everything():
    global calculator_check, file_explorer_check, start_menu_open

    CMD.cmd_deactivate()
    Notepad.notepad_deactivate()
    Calculator.turn_off_calculator()
    File_Explorer.close_file_explorer()

    start_menu.hide_all()
    start_menu_open = 0

    if login_window and login_window.isVisible():
        login_window.hide()

    calculator_check = 0
    file_explorer_check = 0
    File_Explorer._if_open = False

def shutdown_on():
    startbutton.setEnabled(False)
    start_menu.panel.setEnabled(False)
    desktop.setEnabled(False)

    kill_everything()

    # Show shutdown graphics
    startup_bg.raise_()
    shutdowntext.raise_()
    startup_bg.show()
    shutdowntext.show()

    # Force UI to repaint immediately
    QApplication.processEvents()

    # Delay actual quit so user can see shutdown, then cleanly turn off apps
    def _finish_shutdown():
        kill_everything()
        QApplication.quit()

    

    QTimer.singleShot(2000, _finish_shutdown)

# --- Connect to shutdown button ---
shutdownhitbox.clicked.connect(shutdown_on)

# Create start menu controller
start_menu = StartMenu(
    central,
    shutdown_on,
    app_opened_callback=on_app_opened_from_start_menu
)



#Startup gif
startup = QLabel(central)
startup.setAlignment(Qt.AlignCenter)
startup.setGeometry(0, 0, width, height)
startup.setStyleSheet("background-color: black;")

movie = QMovie(asset_path("Real assets", "LOTON startup", "LOTON startup 2.gif"))
startup.setMovie(movie)
movie.finished.connect(startup.hide)

if USING_BOOT_SPLASH:
    startup.hide()
else:
    movie.start()
    startup.raise_()

#Showing the desktop
def show_desktop():
    startup.hide()
    startup_bg.hide()

checkifstartmenuison = 0

# definitions
def backup_shutdown():
    shutdown_on()

def quit_without_shutdown():
    kill_everything()
    QApplication.quit()

def App_preload():
    Loading_Screen.update_loading_text("Warming up Calculator...")
    Calculator.turn_on_calculator()
    Calculator.turn_off_calculator()
    Loading_Screen.update_loading_text("Warming up Notepad...")
    Notepad.notepad_activate()
    Notepad.notepad_deactivate()
    Loading_Screen.update_loading_text("Warming up Command Prompt...")
    CMD.cmd_activate()
    CMD.cmd_deactivate()
    Loading_Screen.update_loading_text("Warming up File Explorer...")
    File_Explorer.open_file_explorer()
    File_Explorer.close_file_explorer()
    Loading_Screen.update_loading_text("Warming up Start Menu...")
    start_menu.show_all()
    start_menu.hide_all()


def finish_startup():
    Loading_Screen.update_loading_text("Booting LOTON...")
    show_desktop()
    QApplication.processEvents()
    Loading_Screen.close_loading_screen()

def calculator_activate():
    global calculator_check
    if calculator_check == 0:
        calculator_check = 1
        Calculator.turn_on_calculator()
    else:
        Calculator.turn_off_calculator()
        calculator_check = 0


def startmenu_on():
    global start_menu_open

    if start_menu_open == 0:
        start_menu.show_all()
        start_menu_open = 1
    else:
        start_menu.hide_all()
        start_menu_open = 0

    


def showhitbox():
    file_explorer_hitbox.show()


def file_explorer_on():
    global file_explorer_check
    if file_explorer_check == 0:
        file_explorer_check = 1
    else:
        file_explorer_check = 0

def desktop_showing_everything():
    background.show()
    folder.show()
    notepad_button.show()
    notepad_hitbox.show()
    calculator_button.show()
    calculator_hitbox.show()
    file_explorer_hitbox.show()
    Loton_store.show()
    cmd_button.show()
    cmd_hitbox.show()
    taskbar.show()
    startbutton.show()
    background.lower()
    taskbar.raise_()
    startbutton.raise_()
    folder.raise_()
    Loton_store.raise_()
    notepad_button.raise_()
    calculator_button.raise_()
    notepad_hitbox.raise_()
    calculator_hitbox.raise_()
    file_explorer_hitbox.raise_()
    cmd_button.raise_()
    cmd_hitbox.raise_()
    start_menu.raise_()

def open_start_menu(self):
    if not hasattr(self, "start_menu"):
        self.start_menu = StartMenu(self)

    # MAIN window position on screen
    main_pos = self.mapToGlobal(self.rect().topLeft())

    x = main_pos.x() + 10
    y = main_pos.y() + self.height() - self.start_menu.height() - 10

    self.start_menu.move(x, y)
    self.start_menu.show()

    
def main_show_everything():
    Loading_Screen.update_loading_text("Preparing LOTON desktop...")
    desktop_showing_everything()
    App_preload()

    remaining_delay_ms = (
        Loading_Screen.remaining_minimum_delay_ms()
        if USING_BOOT_SPLASH
        else 0
    )

    if remaining_delay_ms > 0:
        Loading_Screen.update_loading_text("Finalizing startup...")
        QTimer.singleShot(remaining_delay_ms, finish_startup)
    else:
        finish_startup()
    

#Every assets

#CMD button
cmd_button = QLabel(central)
cmd_path = asset_path("Real assets", "CMD", "CMD icon.png")
cmd_button.setPixmap(QPixmap(cmd_path))
cmd_button.setAttribute(Qt.WA_TransparentForMouseEvents, True)
cmd_button.setGeometry(580, 995, 70, 70)
CMD.cmd_deactivate()
cmd_button.hide()

#CMD hitbox
cmd_hitbox = QPushButton(central)
cmd_hitbox.setGeometry(580, 995, 70, 70)
cmd_hitbox.setStyleSheet("""
    background-color: rgba(0,0,0,0);
    border: none;
""")
cmd_hitbox.clicked.connect(CMD.cmd_activate)
cmd_hitbox.hide()

#Notepad button
notepad_button = QLabel(central)
np_path = asset_path("Real assets", "Notepad", "Notepad Icon 64x64.png")
notepad_button.setPixmap(QPixmap(np_path))
notepad_button.setAttribute(Qt.WA_TransparentForMouseEvents, True)
notepad_button.setGeometry(465, 995, 70, 70)
Notepad.notepad_deactivate()
notepad_button.hide()

# Notepad hitbox
notepad_hitbox = QPushButton(central)
notepad_hitbox.setGeometry(465, 995, 70, 70)
notepad_hitbox.setStyleSheet("""
    background-color: rgba(0,0,0,0);
    border: none;
""")
notepad_hitbox.clicked.connect(Notepad.notepad_activate)
notepad_hitbox.hide()

#Calculator button
calculator_button = QLabel(central)
cl_path = asset_path("Real assets", "Calculator", "Calculator button.png")
calculator_button.setPixmap(QPixmap(cl_path))
calculator_button.setAttribute(Qt.WA_TransparentForMouseEvents, True)
calculator_button.setGeometry(350, 995, 70, 70)
Calculator.turn_off_calculator()
calculator_button.hide()

#Calculator hitbox
calculator_hitbox = QPushButton(central)
calculator_hitbox.setGeometry(350, 995, 70, 70)
calculator_hitbox.setStyleSheet("""
    background-color: rgba(0,0,0,0);
    border: none;
""")
calculator_hitbox.clicked.connect(calculator_activate)
calculator_hitbox.hide()

#File Explorer hitbox
file_explorer_hitbox = QPushButton(central)
file_explorer_hitbox.setGeometry(120, 995, 70, 70)
file_explorer_hitbox.setStyleSheet("""
    background-color: transparent;
    border: none;
    color: transparent;
""")
file_explorer_hitbox.hide()
file_explorer_hitbox.clicked.connect(File_Explorer.open_file_explorer)

#start button
startbutton = QLabel(central)
sb_path = asset_path("Real assets", "Icons", "Resized", "Loton Start Button.png")
startbutton.setPixmap(QPixmap(sb_path))
startbutton.setScaledContents(True)
startbutton.setGeometry(10, 995, 70, 70)
# make the label accept clicks and show a pointer cursor
startbutton.setAttribute(Qt.WA_TransparentForMouseEvents, False)
startbutton.setCursor(Qt.PointingHandCursor)

# clicking the start button toggles the start menu
startbutton.setAttribute(Qt.WA_TransparentForMouseEvents, False)
startbutton.setCursor(Qt.PointingHandCursor)
def _start_button_press(event):
    if event.button() == Qt.LeftButton:
        startmenu_on()
    event.accept()
startbutton.mousePressEvent = _start_button_press
startbutton.show()
startbutton.hide()

#folder
folder = QLabel(central)
f_path = asset_path("Real assets", "File Explorer resized.png")
folder.setPixmap(QPixmap(f_path))
folder.setGeometry(120, 995, 70, 70)
folder.setAttribute(Qt.WA_TransparentForMouseEvents, True)
folder.hide()


Loton_store = QLabel(central)
ls_path = asset_path("Real assets", "Icons", "Resized", "Loton Store.png")
Loton_store.setPixmap(QPixmap(ls_path))
Loton_store.setGeometry(230, 995, 70, 70)
Loton_store.setAttribute(Qt.WA_TransparentForMouseEvents, True)
Loton_store.hide()



taskbar = QLabel(central)
tb_path = asset_path("Real assets", "Taskbar.png")
taskbar.setPixmap(QPixmap(tb_path))
taskbar.setGeometry(0, height - 96, width, 96)
taskbar.hide()

background = QLabel(central)
bg_path = asset_path("Real assets", "Lotonbackground.png")
if Path(bg_path).exists():
    background.setPixmap(QPixmap(bg_path))
else:
    (f"Background image not found: {bg_path}")
background.setGeometry(0, 0, width, height)
background.hide()

startup_bg.setMouseTracking(True)
background.setMouseTracking(True)
central.setMouseTracking(True)
def mouse_move(event):
    global mouse_x, mouse_y
    mouse_x = event.globalPosition().x()
    mouse_y = event.globalPosition().y()

central.mouseMoveEvent = mouse_move


# Kick off the real desktop build as soon as possible when the PyInstaller
# splash is active; otherwise keep the existing in-app intro delay.
startup_delay_ms = 0 if USING_BOOT_SPLASH else SOURCE_STARTUP_DELAY_MS
QTimer.singleShot(startup_delay_ms, main_show_everything)

# Show desktop window
desktop.showFullScreen()
# Run app
File_Explorer._if_open = False
File_Explorer._explorer_instance = None
sys.exit(Loton.exec())
