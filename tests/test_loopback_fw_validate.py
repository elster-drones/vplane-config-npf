import subprocess
from pathlib import Path


def test_rejection_is_written_to_stderr(tmp_path):
    script = Path(__file__).parents[1] / "scripts/loopback-fw-validate"
    result = subprocess.run(
        ["bash", str(script), "dp0p1s0"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert result.stdout == ""
    assert "Firewalls can only be assigned to 'lo'" in result.stderr
    assert list(tmp_path.iterdir()) == []
