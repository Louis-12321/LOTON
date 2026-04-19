# LOTON OS
# Copyright (c) 2026 Louis
# Licensed under the MIT License
#___________________________________________________________________________________________________________________
import sys
from pathlib import Path

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

def resource_path(*parts):
    if getattr(sys, 'frozen', False):
        return str(Path(sys._MEIPASS).joinpath(*parts))
    else:
        return str(Path(__file__).resolve().parents[2].joinpath(*parts))
