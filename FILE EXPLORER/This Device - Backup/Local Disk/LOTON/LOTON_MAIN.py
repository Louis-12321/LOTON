# LOTON OS
# Copyright (c) 2026 Louis
# Licensed under the MIT License
#___________________________________________________________________________________________________________________
import Loading_Screen

Loading_Screen.update_loading_text("Importing PySide6 widgets...")
#Pyside6 imports
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
Loading_Screen.update_loading_text("Importing PySide6 graphics...")
from PySide6.QtGui import QPixmap, QMovie
Loading_Screen.update_loading_text("Importing PySide6 core...")
from PySide6.QtCore import Qt, QTimer
#Other imports
import sys
from pathlib import Path

Loading_Screen.update_loading_text("Starting LOTON...")
import Calculator
Loading_Screen.update_loading_text("Loading Command Prompt...")
import CMD
Loading_Screen.update_loading_text("Loading Notepad...")
import Notepad
Loading_Screen.update_loading_text("Loading File Explorer...")
import File_Explorer
Loading_Screen.update_loading_text("Loading Start Menu...")
from Start_Menu import StartMenu
from Taskbar import Taskbar
Loading_Screen.update_loading_text("Loading login screen...")
import Login
Loading_Screen.update_loading_text("Preparing LOTON desktop...")
import PySide6 #Js a random timer :D

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
# Oh btw 



USING_BOOT_SPLASH = Loading_Screen.is_boot_splash_available()
SOURCE_STARTUP_DELAY_MS = 3000

#Variables
file_explorer_check = 0
calculator_check = 0


shutdowntextwidth = 1080
shutdowntextheight = 145
shutdowntextx = 420
shutdowntexty = 467


#Window move vars
window_x = 478
window_y = 240
mouse_x = 0
mouse_y = 0
offset_x = 0
offset_y = 0
is_dragging = 0
new_x = 0
new_y = 0

Loading_Screen.update_loading_text("Creating LOTON shell...")
Loton = QApplication(sys.argv)
Loading_Screen.update_loading_text("Opening login screen...")
login_window = Login.login_activate()  # Runs the login window on top of the desktop app
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
desktop.setWindowTitle("Loton OS v1.1.0.0")
desktop.setGeometry(0, 0, width, height)

central = QWidget(desktop)
desktop.setCentralWidget(central)   

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

# --- Shutdown function ---

def kill_everything():
    global calculator_check, file_explorer_check

    CMD.cmd_deactivate()
    Notepad.notepad_deactivate()
    Calculator.turn_off_calculator()

    if file_explorer_check == 1:
        window.hide()
        file_explorer_check = 0

    start_menu.hide_all()
    taskbar.start_menu_open = 0

    if login_window and login_window.isVisible():
        login_window.hide()

    calculator_check = 0

def shutdown_on():
    taskbar.startbutton.setEnabled(False)
    start_menu.panel.setEnabled(False)
    desktop.setEnabled(False)

    kill_everything()

    startup_bg.raise_()
    shutdowntext.raise_()
    startup_bg.show()
    shutdowntext.show()

    QApplication.processEvents()

    def _finish_shutdown():
        kill_everything()
        QApplication.quit()

    QTimer.singleShot(2000, _finish_shutdown)

# Create start menu controller
start_menu = StartMenu(
    central,
    shutdown_on,
    app_opened_callback=None
)

taskbar = Taskbar(
    central=central,
    width=width,
    height=height,
    start_menu=start_menu,
    calculator_callback=calculator_activate,
    file_explorer_callback=file_explorer_on,
    cmd_callback=CMD.cmd_activate,
    notepad_callback=Notepad.notepad_activate,
    shutdown_callback=shutdown_on
)

start_menu.app_opened_callback = taskbar.on_app_opened



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


def finish_startup():
    Loading_Screen.update_loading_text("Opening LOTON...")
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




def file_explorer_on():
    global file_explorer_check
    if file_explorer_check == 0:
        window.show()
        file_explorer_check = 1
    else:
        window.hide()
        file_explorer_check = 0



def mouse_release(event):
    global is_dragging
    is_dragging = 0
    ("Stopped dragging")


def window_click_on():
    ("Clicked")

#Window go movy movy ye :D
def drag_start(event):
    global offset_x, offset_y, is_dragging
    is_dragging = 1
    offset_x = event.globalPosition().x() - window.x()
    offset_y = event.globalPosition().y() - window.y()

def drag_stop(event):
    global is_dragging
    is_dragging = 0

def drag(event):
    global is_dragging, new_x, new_y, offset_x, offset_y
    if is_dragging == 1:
        pos = event.globalPosition().toPoint()
        new_x = pos.x() - offset_x
        new_y = pos.y() - offset_y
        window.move(new_x, new_y)
        window.update()

#update the window UI every frame
def update_window_ui():
    if hasattr(window, "title_bar"):
        window.title_bar.resize(window.width(), 36)
    
def desktop_showing_everything():
    background.show()
    taskbar.show_all()
    background.lower()
    start_menu.raise_()

    
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
    

#Window
window = File_Explorer.FileExplorer(central)
window.setGeometry(window_x, window_y, 964, 601)
window.hide()

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
window.setMouseTracking(True)
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
sys.exit(Loton.exec())
