# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE.md file for details.
#______________________________________________________________________________________

import json
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QWidget

CURRENT_THEME = "Default"
_previous_theme = "Default"
_theme_timer = None
_last_saved_theme = None
_applying_theme = False
_theme_callbacks = {}
THEME_FILE = Path(__file__).resolve().parent / "theme_settings.json"


THEME_REPLACEMENTS = {
    "Default": {},
    "Dark": {
        "#003eff": "#141820",
        "#18039E": "#141820",
        "#00003C": "#0b0f16",
        "#002bbd": "#0b0f16",
        "#0040ff": "#2b3445",
        "#0058ff": "#252d3a",
        "#0078ff": "#35445c",
        "#0066ff": "#41526d",
        "#0055ff": "#35445c",
        "#006eff": "#35445c",
        "#2d73ff": "#41526d",
        "#426cf5": "#1d2430",
        "#4266f5": "#1d2430",
        "#0380fc": "#252d3a",
        "#0223aa": "#1d2430",
        "#0022ff": "#171d28",
        "#002fff": "#252d3a",
        "#0084ff": "#35445c",
        "#00a6ff": "#41526d",
        "#0d00c2": "#101722",
        "#0f49ff": "#1d2430",
        "#1100ff": "#171d28",
        "#001f8f": "#101722",
        "#1492ff": "#35445c",
        "#39a6ff": "#41526d",
        "#6fa8ff": "#596579",
        "#8fd9ff": "#596579",
        "#9bc5ff": "#6b7890",
        "#b8ebff": "#6b7890",
        "#9dd2ff": "#b8c7df",
        "#d2efff": "#d9e4f5",
        "#cddfff": "#b8c7df",
        "#f5f8ff": "#252d3a",
        "#d7e6ff": "#4c596d",
        "#dceaff": "#313b4c",
        "#0030a8": "#ffffff",
        "color: white": "color: white",
        "color: White": "color: White",
        "color:#888": "color:#b8c7df",
        "color: rgba(255, 255, 255, 180)": "color: rgba(255, 255, 255, 180)",
        "rgba(50, 100, 220, 200)": "rgba(20, 30, 50, 200)",
        "rgba(255, 255, 255, 50)": "rgba(255, 255, 255, 15)",
        "rgba(255, 255, 255, 72)": "rgba(255, 255, 255, 25)",
        "rgba(0, 43, 189, 150)": "rgba(11, 15, 22, 150)",
        "rgba(157, 210, 255, 95)": "rgba(89, 101, 121, 95)",
        "rgba(157, 210, 255, 80)": "rgba(89, 101, 121, 80)",
        "rgba(157, 210, 255, 110)": "rgba(89, 101, 121, 110)",
        "rgba(157, 210, 255, 120)": "rgba(89, 101, 121, 120)",
        "rgba(0, 78, 255, 180)": "rgba(50, 50, 55, 180)",
        "rgba(0, 120, 255, 220)": "rgba(65, 65, 72, 220)",
        "rgba(8, 55, 180, 200)": "rgba(13, 16, 25, 200)",
        "rgba(255, 255, 255, 28)": "rgba(255, 255, 255, 10)",
        "rgba(255, 255, 255, 150)": "rgba(255, 255, 255, 80)",
        "rgba(255, 255, 255, 220)": "rgba(255, 255, 255, 220)",
        "rgba(255, 255, 255, 160)": "rgba(255, 255, 255, 160)",
        "rgba(255, 255, 255, 190)": "rgba(255, 255, 255, 190)",
    },
    "Light": {
        "#003eff": "#eaf3ff",
        "#18039E": "#eaf3ff",
        "#00003C": "#d7e9ff",
        "#002bbd": "#bcd8ff",
        "#0040ff": "#9ec7ff",
        "#0058ff": "#f8fbff",
        "#0078ff": "#8dbbff",
        "#0066ff": "#73a9fa",
        "#0055ff": "#8dbbff",
        "#2d73ff": "#73a9fa",
        "#426cf5": "#d7e9ff",
        "#4266f5": "#d7e9ff",
        "#0380fc": "#f8fbff",
        "#0223aa": "#d7e9ff",
        "#0022ff": "#dcecff",
        "#002fff": "#8dbbff",
        "#0040ff": "#9ec7ff",
        "#0055ff": "#8dbbff",
        "#0058ff": "#f8fbff",
        "#0066ff": "#73a9fa",
        "#006eff": "#8dbbff",
        "#0078ff": "#8dbbff",
        "#0084ff": "#8dbbff",
        "#00a6ff": "#73a9fa",
        "#0d00c2": "#c9e0ff",
        "#0f49ff": "#d7e9ff",
        "#1100ff": "#dcecff",
        "#001f8f": "#dcecff",
        "#1492ff": "#8dbbff",
        "#39a6ff": "#73a9fa",
        "#6fa8ff": "#78adff",
        "#8fd9ff": "#9fc4f6",
        "#9bc5ff": "#dcecff",
        "#b8ebff": "#dcecff",
        "#9dd2ff": "#234c85",
        "#d2efff": "#234c85",
        "#cddfff": "#234c85",
        "#f5f8ff": "#f8fbff",
        "#d7e6ff": "#9fc4f6",
        "#dceaff": "#dcecff",
        "#0030a8": "#061735",
        "color: white": "color: #061735",
        "color: White": "color: #061735",
        "color:#fff": "color:#061735",
        "color: #fff": "color: #061735",
        "color:#888": "color:#234c85",
        "color: rgba(255, 255, 255, 180)": "color: rgba(0, 0, 0, 180)",
        "rgba(50, 100, 220, 200)": "rgba(210, 225, 250, 200)",
        "rgba(255, 255, 255, 50)": "rgba(0, 0, 0, 30)",
        "rgba(255, 255, 255, 72)": "rgba(0, 0, 0, 40)",
        "rgba(0, 43, 189, 150)": "rgba(188, 216, 255, 150)",
        "rgba(157, 210, 255, 95)": "rgba(120, 173, 255, 95)",
        "rgba(157, 210, 255, 80)": "rgba(120, 173, 255, 80)",
        "rgba(157, 210, 255, 110)": "rgba(120, 173, 255, 110)",
        "rgba(157, 210, 255, 120)": "rgba(120, 173, 255, 120)",
        "rgba(0, 78, 255, 180)": "rgba(158, 199, 255, 180)",
        "rgba(0, 120, 255, 220)": "rgba(180, 215, 255, 220)",
        "rgba(8, 55, 180, 200)": "rgba(232, 243, 255, 200)",
        "rgba(255, 255, 255, 28)": "rgba(0, 0, 0, 20)",
        "rgba(255, 255, 255, 150)": "rgba(0, 0, 0, 80)",
        "rgba(255, 255, 255, 220)": "rgba(0, 0, 0, 180)",
        "rgba(255, 255, 255, 160)": "rgba(0, 0, 0, 120)",
        "rgba(255, 255, 255, 190)": "rgba(0, 0, 0, 150)",
    },
}


def _replace_stylesheet(original, theme_name):
    stylesheet = original
    replacements = THEME_REPLACEMENTS.get(theme_name, {})

    for old, new in replacements.items():
        stylesheet = stylesheet.replace(old, new)

    return stylesheet


def _apply_stylesheet(widget, stylesheet, theme_name):
    original = widget.property("_loton_original_stylesheet")
    if original is None:
        original = stylesheet
        widget.setProperty("_loton_original_stylesheet", original)
    elif original != stylesheet:
        expected = _replace_stylesheet(original, _previous_theme)
        if stylesheet != expected:
            widget.setProperty("_loton_original_stylesheet", stylesheet)
            original = stylesheet
    widget.setStyleSheet(_replace_stylesheet(original, theme_name))


def _apply_to_widget(widget, theme_name):
    if not isinstance(widget, QWidget):
        return

    try:
        stylesheet = widget.styleSheet()
    except RuntimeError:
        return

    if stylesheet:
        try:
            _apply_stylesheet(widget, stylesheet, theme_name)
        except RuntimeError:
            return

    try:
        children = widget.findChildren(QWidget)
    except RuntimeError:
        return

    for child in children:

        try:
            child_stylesheet = child.styleSheet()
        except RuntimeError:
            continue

        if not child_stylesheet:
            continue

        try:
            _apply_stylesheet(child, child_stylesheet, theme_name)
        except RuntimeError:
            continue


def save_theme(theme_name):
    try:
        THEME_FILE.write_text(
            json.dumps({"theme": theme_name}, indent=4),
            encoding="utf-8"
        )
    except OSError:
        pass


def load_saved_theme():
    try:
        data = json.loads(THEME_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "Default"

    theme_name = data.get("theme", "Default")
    if theme_name not in THEME_REPLACEMENTS:
        return "Default"

    return theme_name


def apply_theme_to_open_windows(theme_name):
    global _applying_theme

    if _applying_theme:
        return

    app = QApplication.instance()
    if app is None:
        return

    _applying_theme = True
    try:
        for widget in app.topLevelWidgets():
            _apply_to_widget(widget, theme_name)
    finally:
        _applying_theme = False


def apply_saved_theme():
    global CURRENT_THEME, _last_saved_theme, _previous_theme

    _previous_theme = CURRENT_THEME
    CURRENT_THEME = load_saved_theme()
    _last_saved_theme = CURRENT_THEME
    apply_theme_to_open_windows(CURRENT_THEME)


def install_theme_sync(interval_ms=500):
    global _theme_timer, _last_saved_theme

    app = QApplication.instance()
    if app is None:
        return

    apply_saved_theme()

    if _theme_timer is not None:
        return

    _last_saved_theme = CURRENT_THEME
    _theme_timer = QTimer(app)

    def sync_theme():
        global CURRENT_THEME, _last_saved_theme

        saved_theme = load_saved_theme()
        if saved_theme == _last_saved_theme:
            return

        CURRENT_THEME = saved_theme
        _last_saved_theme = saved_theme
        apply_theme_to_open_windows(saved_theme)

    _theme_timer.timeout.connect(sync_theme)
    _theme_timer.start(interval_ms)


def register_theme_callback(key, callback):
    _theme_callbacks[key] = callback


def set_theme(theme_name):
    global CURRENT_THEME, _last_saved_theme, _previous_theme

    _previous_theme = CURRENT_THEME
    CURRENT_THEME = theme_name
    _last_saved_theme = theme_name
    save_theme(theme_name)
    apply_theme_to_open_windows(CURRENT_THEME)
    for callback in _theme_callbacks.values():
        callback(theme_name)


def apply_theme_images(theme_name):
    for callback in _theme_callbacks.values():
        callback(theme_name)
