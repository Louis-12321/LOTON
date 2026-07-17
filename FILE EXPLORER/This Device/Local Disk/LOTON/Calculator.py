# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE.md file for details.
#______________________________________________________________________________________

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QGridLayout, QPushButton
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainterPath
import sys
import math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from Theme_Manager import install_theme_sync

WIDTH = 350
HEIGHT = 470
RADIUS = 16

# ===============================
# HELPERS
# ===============================
def format_number(value):
    if isinstance(value, float):
        return f"{value:.8f}".rstrip("0").rstrip(".")
    return str(value)


# ===============================
# GLOBAL INSTANCE
# ===============================
_calc_instance = None


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        # ===== Window =====
        self.setWindowTitle("LOTON Calculator")
        self.resize(WIDTH, HEIGHT)
        self.setMinimumSize(320, 240)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # keep calculator on top of other windows
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        # ===== Root =====
        self.root = QWidget(self)
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.root.setStyleSheet("""
            QWidget {
                background-color: #003eff;
                border-radius: 16px;
            }
        """)

        # ===== Title Bar ===== 
        self.title_bar = QWidget(self.root)
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("""
            background-color: #002bbd;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        """)
        self.title_bar.installEventFilter(self)

        title_layout = QGridLayout(self.title_bar)
        title_layout.setContentsMargins(8, 0, 8, 0)

        title = QLabel("LOTON Calculator")
        title.setStyleSheet("color:white; font-size:14px;")

        btn_min = QPushButton("—")
        btn_close = QPushButton("✕")

        for btn in (btn_min, btn_close):
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

        btn_min.clicked.connect(self.showMinimized)
        btn_close.clicked.connect(self.hide)

        title_layout.addWidget(title, 0, 0)
        title_layout.addWidget(btn_min, 0, 1)
        title_layout.addWidget(btn_close, 0, 2)
        title_layout.setColumnStretch(0, 1)

        # ===== History =====
        self.history = QLabel("")
        self.history.setAlignment(Qt.AlignRight)
        self.history.setStyleSheet("color:#888; font-size:16px; padding:6px;")

        # ===== Display =====
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet("""
            font-size: 36px;
            padding: 12px;
            background-color: #0058ff;
            color: white;
            border-radius: 10px;
        """)

        # ===== Buttons =====
        grid = QGridLayout()
        grid.setSpacing(10) 
        self.grid = grid

        buttons = [
            ("C", 0, 0), ("⌫", 0, 1), ("√", 0, 2), ("/", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("*", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2, 1, 2),
        ]

        # metadata list for responsive sizing
        self.button_meta = []

        for text, row, col, *span in buttons:
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.NoFocus)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    background-color: #0078ff;
                    color: white;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #0066ff;
                }
            """)
            btn.clicked.connect(lambda _, t=text: self.button_pressed(t))

            rowspan = span[0] if span else 1
            colspan = span[1] if span else 1
            self.button_meta.append({
                'btn': btn,
                'row': row,
                'col': col,
                'rowspan': rowspan,
                'colspan': colspan,
                'text': text,
            })

            if span:
                grid.addWidget(btn, row, col, span[0], span[1])
            else:
                grid.addWidget(btn, row, col)

        # ===== Layout =====
        layout = QVBoxLayout(self.root)
        layout.setContentsMargins(8, 6, 8, 8)
        layout.setSpacing(6)
        self.main_layout = layout

        layout.addWidget(self.title_bar)
        layout.addWidget(self.history)
        layout.addWidget(self.display)
        layout.addLayout(grid)

        # Resize grip (visual)
        self.resize_handle = QWidget(self.root)
        self.resize_handle.setFixedSize(18, 18)
        self.resize_handle.setStyleSheet("""
            background-color: #6fa8ff;
            border-radius: 6px;
        """)
        self.resize_handle.setCursor(Qt.SizeFDiagCursor)

        # Layout update and mask
        self.update_layout()
        # Compute and enforce a minimum height based on content so buttons won't break
        min_h = self.compute_min_height()
        self.setMinimumSize(320, min_h)
        self.resizing = False

        # ===== State =====
        self.expression = ""
        self.eval_expr = ""
        self.last_answer = None
        self.just_calculated = False
        self.drag_pos = None
        install_theme_sync()

    # ===== Drag =====
    def eventFilter(self, obj, event):
        if obj == self.title_bar:
            if event.type() == QEvent.MouseButtonPress:
                self.drag_pos = event.globalPosition().toPoint()
                return True
            if event.type() == QEvent.MouseMove and event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
                self.drag_pos = event.globalPosition().toPoint()
                return True
        return super().eventFilter(obj, event)

    # ===== Keyboard =====
    def keyPressEvent(self, event):
        if self.expression == "Error" and event.key() != Qt.Key_C:
            return

        if event.key() == Qt.Key_Backspace:
            self.backspace()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.calculate()
        elif event.text() in "0123456789.+-*/":
            if self.just_calculated and event.text() not in "+-*/":
                return
            self.input_text(event.text())

        self.update_display()

    # ===== Logic =====
    def button_pressed(self, text):
        if self.expression == "Error" and text != "C":
            return

        if text == "C":
            self.clear()
        elif text == "⌫":
            self.backspace()
        elif text == "=":
            self.calculate()
        elif text == "√":
            target = self.expression or self.last_answer or 0
            self.expression = f"√({target})"
            self.eval_expr = f"math.sqrt({target})"
        else:
            if self.just_calculated and text not in "+-*/":
                return
            self.input_text(text)

        self.update_display()

    def backspace(self):
        self.expression = self.expression[:-1]
        self.eval_expr = self.eval_expr[:-1]
        self.just_calculated = False

    def input_text(self, text):
        self.expression += text
        self.eval_expr += text
        self.just_calculated = False

    def calculate(self):
        try:
            result = eval(self.eval_expr, {"math": math})
            self.history.setText(self.expression)
            self.last_answer = result
            self.expression = format_number(result)
            self.eval_expr = str(result)
            self.just_calculated = True
        except Exception as e:
            print(f"Calculator error: {e}")
            self.expression = "Error"
            self.eval_expr = ""

    def clear(self):
        self.expression = ""
        self.eval_expr = ""
        self.history.setText("")
        self.just_calculated = False

    def update_display(self):
        self.display.setText(self.expression or "0")

    # ---- layout + mask ----
    def update_layout(self):
        self.root.setGeometry(0, 0, self.width(), self.height())
        self.title_bar.setGeometry(0, 0, self.width(), 36)

        self.resize_handle.move(
            self.width() - self.resize_handle.width() - 6,
            self.height() - self.resize_handle.height() - 6
        )

        self.apply_mask()
        # update button sizes to match current widget geometry
        if hasattr(self, 'button_meta'):
            self.update_button_sizes()

    def apply_mask(self):
        path = QPainterPath()
        path.addRoundedRect(self.rect(), RADIUS, RADIUS)
        self.setMask(path.toFillPolygon().toPolygon())

    def compute_min_height(self):
        """Compute the minimum usable height based on the title bar, history, display
        and the button grid so resizing cannot shrink the window until the buttons break.
        """
        # fixed counts and sizes coming from the default styles
        rows = 5
        btn_h = 50
        grid_spacing = self.grid.spacing() if hasattr(self, 'grid') else 10

        grid_height = rows * btn_h + (rows - 1) * grid_spacing

        title_h = self.title_bar.height() if self.title_bar.isVisible() else 36
        history_h = max(20, self.history.sizeHint().height())
        display_h = max(56, self.display.sizeHint().height())

        # layout-level spacing: there are 3 gaps above the grid (title->history->display->grid)
        layout_spacing = self.main_layout.spacing() if hasattr(self, 'main_layout') else 6
        total_main_gaps = layout_spacing * 3

        margins = self.main_layout.contentsMargins() if hasattr(self, 'main_layout') else (8, 6, 8, 8)
        top_margin = margins.top() if hasattr(margins, 'top') else margins[1]
        bottom_margin = margins.bottom() if hasattr(margins, 'bottom') else margins[3]

        # Additional padding to account for borders/rounded corners/resize handle
        extra = 16

        total = top_margin + title_h + layout_spacing + history_h + layout_spacing + display_h + total_main_gaps + grid_height + bottom_margin + extra
        return total

    def update_button_sizes(self):
        """Compute and apply button sizes so grid fills available space and gaps remain equal.
        This method is conservative and enforces minimums so it doesn't break the layout.
        """
        # Basic parameters
        spacing = self.grid.spacing() if hasattr(self, 'grid') else 10
        margins = self.main_layout.contentsMargins() if hasattr(self, 'main_layout') else None

        # Horizontal (columns)
        content_width = self.root.width() - (margins.left() + margins.right()) if margins else self.root.width()
        cols = 4
        available_width = max(0, content_width - spacing * (cols - 1))
        base_w = max(44, available_width // cols)
        remainder = max(0, available_width - base_w * cols)
        col_widths = [base_w + (1 if i < remainder else 0) for i in range(cols)]

        # Vertical (rows)
        title_h = self.title_bar.height()
        history_h = self.history.sizeHint().height()
        display_h = self.display.sizeHint().height()
        main_spacing = self.main_layout.spacing()
        content_height = self.root.height() - (
            title_h + history_h + display_h + main_spacing * 3 + (margins.top() + margins.bottom() if margins else 0)
        )
        rows = 5
        available_height = max(rows * 28, content_height - spacing * (rows - 1))
        base_h = max(30, available_height // rows)
        rem_h = max(0, available_height - base_h * rows)
        row_heights = [base_h + (1 if i < rem_h else 0) for i in range(rows)]

        # Apply sizes to buttons based on metadata
        for meta in getattr(self, 'button_meta', []):
            col = meta['col']
            colspan = meta['colspan']
            row = meta['row']
            rowspan = meta['rowspan']

            if colspan == 1:
                w = col_widths[col]
            else:
                w = sum(col_widths[col:col+colspan]) + spacing * (colspan - 1)

            h = sum(row_heights[row:row+rowspan]) + spacing * (rowspan - 1)

            # enforce minimums
            w = max(44, w)
            h = max(30, h)

            font_size = max(10, int(min(w, h) * 0.22))
            radius = max(4, int(6 * (h / 50)))

            btn = meta['btn']
            btn.setFixedSize(w, h)
            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: {font_size}px;
                    background-color: #0078ff;
                    color: white;
                    border-radius: {radius}px;
                }}
                QPushButton:hover {{
                    background-color: #0066ff;
                }}
            """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_layout()

    # ---- resizing + dragging ----
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.resize_handle.underMouse():
                self.resizing = True
                self.resize_start = event.globalPosition().toPoint()
                self.start_size = self.size()
                return
            if self.title_bar.underMouse():
                self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if getattr(self, "resizing", False):
            delta = event.globalPosition().toPoint() - self.resize_start
            new_w = max(self.minimumWidth(), self.start_size.width() + delta.x())
            new_h = max(self.minimumHeight(), self.start_size.height() + delta.y())
            self.resize(new_w, new_h)
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.resizing = False


# ===============================
# LOTON CONTROL FUNCTIONS
# ===============================
def turn_on_calculator():
    global _calc_instance

    if QApplication.instance() is None:
        QApplication(sys.argv)

    if _calc_instance is None:
        _calc_instance = Calculator()

    _calc_instance.show()
    _calc_instance.raise_()
    _calc_instance.activateWindow()


def turn_off_calculator():
    global _calc_instance
    if _calc_instance is not None:
        _calc_instance.hide()



# ===============================
# STANDALONE TEST
# ===============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    turn_on_calculator()
    sys.exit(app.exec())
