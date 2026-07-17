# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE.md file for details.
#______________________________________________________________________________________


# MAIN FILE
# Contains Desktop and app management


#region IMPORTS
import Loading_Screen
Loading_Screen.update_loading_text("Initializing LOTON...")
import PySide6 #A timer
Loading_Screen.update_loading_text("Importing PySide6 widgets...")
#Pyside6 imports
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget
Loading_Screen.update_loading_text("Importing PySide6 graphics...")
from PySide6.QtGui import QMovie, QPixmap
Loading_Screen.update_loading_text("Importing PySide6 core...")
from PySide6.QtCore import Qt, QTimer
#System imports
Loading_Screen.update_loading_text("Importing system modules...")
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.append(str(PROJECT_DIR))

#App imports
Loading_Screen.update_loading_text("Starting LOTON...")
import Calculator
Loading_Screen.update_loading_text("Loading Command Prompt...")
import CMD
Loading_Screen.update_loading_text("Loading Notepad...")
import Notepad
Loading_Screen.update_loading_text("Loading Start Menu...")
import Start_Menu
Loading_Screen.update_loading_text("Loading File Explorer...")
import File_Explorer
Loading_Screen.update_loading_text("Loading Account Manager...")
import Account_Manager
Loading_Screen.update_loading_text("Loading login screen...")
import Login
Loading_Screen.update_loading_text("Loading Settings...")
import Settings
Loading_Screen.update_loading_text("Loading Taskbar...")
from Taskbar import Taskbar
#endregion

#region PREP

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


shutdowntextwidth = 1080
shutdowntextheight = 145
shutdowntextx = 420
shutdowntexty = 467


Loading_Screen.update_loading_text("Creating LOTON shell...")
Loton = QApplication(sys.argv)
# Prevent app from quitting when message boxes close while no windows are visible
Loton.setQuitOnLastWindowClosed(False)
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

#endregion

#region WINDOW

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

#endregion

#region GUI & LOGIC

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
    File_Explorer.close_file_explorer()
    Account_Manager.account_manager_deactivate()
    Settings.settings_deactivate()

    start_menu.hide_all()
    taskbar.start_menu_open = 0

    if login_window and login_window.isVisible():
        login_window.hide()

    calculator_check = 0
    file_explorer_check = 0
    File_Explorer._if_open = False

def shutdown_on():
    taskbar.startbutton.setEnabled(False)
    start_menu.panel.setEnabled(False)
    desktop.setEnabled(False)

    taskbar.hide_all()

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

def calculator_activate():
    global calculator_check
    if calculator_check == 0:
        calculator_check = 1
        Calculator.turn_on_calculator()
    else:
        Calculator.turn_off_calculator()
        calculator_check = 0


# Create start menu controller
start_menu = Start_Menu.StartMenu(
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
    notepad_callback=Notepad.notepad_activate,
    cmd_callback=CMD.cmd_activate,
    file_explorer_callback=File_Explorer.open_file_explorer,
    account_manager_callback=Account_Manager.account_manager_activate,
    settings_callback=Settings.settings_activate,
    shutdown_callback=shutdown_on,
    asset_path_func=asset_path
)

start_menu.app_opened_callback = taskbar.on_app_opened

#Showing the desktop
def show_desktop():
    startup_bg.hide()

checkifstartmenuison = 0

# definitions
def backup_shutdown():
    shutdown_on()

def quit_without_shutdown():
    kill_everything()
    QApplication.quit()

def App_preload():
    Loading_Screen.update_loading_text("preloading apps...")
    Calculator.turn_on_calculator()
    Calculator.turn_off_calculator()
    Notepad.notepad_activate()
    Notepad.notepad_deactivate()
    CMD.cmd_activate()
    CMD.cmd_deactivate()
    File_Explorer.open_file_explorer()
    File_Explorer.close_file_explorer()
    Account_Manager.account_manager_activate()
    Account_Manager.account_manager_deactivate()
    Settings.settings_activate()
    QApplication.processEvents()
    Settings.settings_deactivate()


def finish_startup():
    Loading_Screen.update_loading_text("Booting LOTON...")
    show_desktop()
    QApplication.processEvents()
    Loading_Screen.close_loading_screen()

def file_explorer_on():
    global file_explorer_check
    if file_explorer_check == 0:
        file_explorer_check = 1
    else:
        file_explorer_check = 0

def desktop_showing_everything():
    background.show()
    taskbar.show_all()
    background.lower()
    start_menu.raise_()


def main_show_everything():
    Loading_Screen.update_loading_text("Preparing LOTON desktop...")
    desktop_showing_everything()

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
    

def desktop_click(event):
    if taskbar.startbutton.geometry().contains(event.pos()):
        return

    if start_menu.panel.isVisible():
        start_menu.click_outside_close(event.globalPosition().toPoint())

central.mousePressEvent = desktop_click

background = QLabel(central)
bg_path = asset_path("Real assets", "Lotonbackground.png")
if Path(bg_path).exists():
    background.setPixmap(QPixmap(bg_path))
else:
    (f"Background image not found: {bg_path}")
background.setGeometry(0, 0, width, height)
background.hide()

#region PERSONALISATION

def _apply_wallpaper(path):
    pixmap = QPixmap(path)
    if not pixmap.isNull():
        background.setPixmap(pixmap)

def _apply_profile_picture(path):
    pixmap = QPixmap(path)
    if not pixmap.isNull():
        pixmap = pixmap.scaled(144, 144, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        start_menu.userpic.setPixmap(pixmap)

Settings.register_personalisation_appliers(
    wallpaper=_apply_wallpaper,
    show_icons=taskbar.apply_show_icons,
    taskbar_position=taskbar.apply_position,
    profile_picture=_apply_profile_picture,
)

#endregion

startup_bg.setMouseTracking(True)
background.setMouseTracking(True)
central.setMouseTracking(True)
def mouse_move(event):
    global mouse_x, mouse_y
    mouse_x = event.globalPosition().x()
    mouse_y = event.globalPosition().y()

central.mouseMoveEvent = mouse_move

#endregion

#region KICKOFF

# Kick off the real desktop build as soon as possible when the PyInstaller
# splash is active; otherwise keep the existing in-app intro delay.
startup_delay_ms = 0 if USING_BOOT_SPLASH else SOURCE_STARTUP_DELAY_MS
QTimer.singleShot(startup_delay_ms, main_show_everything)

# Show desktop window
desktop.showFullScreen()
#endregion

# Run app
try:
    sys.exit(Loton.exec())
except Exception as e:
    print(f"FATAL ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
