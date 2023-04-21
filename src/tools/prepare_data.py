from typing import Tuple

import numpy as np
import pandas as pd
from evidently.test_preset import DataDriftTestPreset
from evidently.test_suite import TestSuite
from sklearn import datasets


def example_data_drift() -> Tuple[bool, str, bytes]:
    """
    Example from https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_test_presets.ipynb

    Returns:
        True/False whether alert is detected
    """
    # Dataset for Data Quality and Integrity
    adult_data = datasets.fetch_openml(
        name="adult", version=2, as_frame="auto", parser="auto"
    )
    adult = adult_data.frame

    adult_ref = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
    adult_cur = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]

    adult_cur.iloc[:2000, 3:5] = np.nan

    data_drift = TestSuite(
        tests=[
            DataDriftTestPreset(stattest="psi"),
        ]
    )

    data_drift.run(reference_data=adult_ref, current_data=adult_cur)
    # Save the report as HTML
    from tools.helper_functions import get_evidently_html

    html, html_bytes = get_evidently_html(data_drift)

    test_summary = data_drift.as_dict()
    other_tests_summary = []

    failed_tests = []
    for test in test_summary["tests"]:
        if test["status"].lower() == "fail":
            failed_tests.append(test)

    is_alert = any([failed_tests, other_tests_summary])
    print(f"Alert Detected: {is_alert}")

    return is_alert, html, html_bytes
