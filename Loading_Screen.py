"""Startup helpers for LOTON's PyInstaller splash screen."""

from time import perf_counter

DEFAULT_MINIMUM_SPLASH_MS = 6500
_startup_started_at = perf_counter()

try:
    import pyi_splash as _pyi_splash #type: ignore
except Exception:
    _pyi_splash = None


def is_boot_splash_available():
    """Return True when the PyInstaller splash screen is active."""
    return bool(_pyi_splash and getattr(_pyi_splash, "is_alive", lambda: False)())


def update_loading_text(message):
    """Update the PyInstaller splash text when available."""
    if not is_boot_splash_available():
        return

    try:
        _pyi_splash.update_text(message)
    except (ConnectionError, RuntimeError):
        pass


def close_loading_screen():
    """Close the PyInstaller splash screen when it is active."""
    if not is_boot_splash_available():
        return

    try:
        _pyi_splash.close()
    except (ConnectionError, RuntimeError):
        pass


def remaining_minimum_delay_ms(minimum_ms=DEFAULT_MINIMUM_SPLASH_MS):
    """Return the remaining time needed to keep startup visible."""
    elapsed_ms = int((perf_counter() - _startup_started_at) * 1000)
    return max(0, minimum_ms - elapsed_ms)
