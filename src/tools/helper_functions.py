import tempfile
from typing import Tuple


def get_evidently_html(evidently_object) -> Tuple[str, bytes]:
    """Returns the rendered EvidentlyAI report/metric as HTML and binary format"""
    with tempfile.NamedTemporaryFile() as tmp:
        evidently_object.save_html(tmp.name)
        with open(tmp.name) as fh:
            html = fh.read()

        with open(tmp.name, "rb") as fh:
            html_bytes = fh.read()

        return html, html_bytes
