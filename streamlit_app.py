# -*- coding: utf-8 -*-
"""MADYT Hotel Anvelope – VERSIUNE DEMO.

Pornește aplicația (app_core.py) forțat în modul DEMO: fișiere CSV temporare cu date inventate,
fără nicio conexiune la Google Sheets.
"""
import os
import runpy
import tempfile

os.environ["MADYT_DEMO"] = "1"
os.environ["MADYT_DEMO_RICH"] = "1"
os.environ["MADYT_DEMO_BANNER"] = "1"
os.environ["MADYT_SPREADSHEET_ID"] = "DEMO-FARA-GOOGLE-SHEETS"
os.environ.setdefault("MADYT_DEMO_DIR", os.path.join(tempfile.gettempdir(), "madyt_demo_data"))

runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_core.py"), run_name="__main__")
