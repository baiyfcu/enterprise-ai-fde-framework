import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_cli_outputs_json():
    completed = subprocess.run(
        [sys.executable, "-m", "app.cli"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    body = json.loads(completed.stdout)
    assert body["requirement"]["industry"] == "制造业"
    assert body["delivery"]["executive_summary"]
