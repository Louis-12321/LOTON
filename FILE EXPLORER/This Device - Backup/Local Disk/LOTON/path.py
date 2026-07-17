# LOTON OS
# Copyright (c) 2026 Louis
#
# This project is licensed under the MIT License.
# See LICENSE file for details.
#____________________________________________________________________________________________________________
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
