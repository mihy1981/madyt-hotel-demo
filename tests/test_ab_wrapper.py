"""Rulează aplicația DEMO exact cum pornește pe Streamlit Cloud (streamlit_app.py)."""
import os
import tempfile

from streamlit.testing.v1 import AppTest

WRAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "streamlit_app.py")


def test_wrapper_rich_demo():
    d = tempfile.mkdtemp()
    old = {k: os.environ.get(k) for k in ("MADYT_DEMO_DIR", "MADYT_DEMO", "MADYT_DEMO_RICH", "MADYT_DEMO_BANNER", "MADYT_SPREADSHEET_ID")}
    os.environ["MADYT_DEMO_DIR"] = d
    try:
        at = AppTest.from_file(WRAP, default_timeout=180)
        at.run()
        assert not at.exception, [e.value for e in at.exception]
        assert len(at.tabs) >= 18, len(at.tabs)
        assert any("DEMO" in i.value for i in at.info)
        assert not [w.value for w in at.warning if "incomplete" in w.value]
        files = set(os.listdir(d))
        for t in ("Comenzi.csv", "Miscari.csv", "Facturare.csv", "Masini.csv", "Clienti.csv"):
            assert t in files, files
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
