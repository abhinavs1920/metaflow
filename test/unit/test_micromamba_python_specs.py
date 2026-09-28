"""Python match specs passed from @conda/@pypi to micromamba."""

import pytest

from metaflow.plugins.pypi.micromamba import Micromamba


@pytest.mark.parametrize(
    "python, expected",
    [
        ("3.11", "python=3.11"),
        ("3.11.0", "python==3.11.0"),
        ("==3.11.5", "python==3.11.5"),
        (">=3.11,<3.12", "python>=3.11,<3.12"),
        ("3.13t", "python=3.13"),
        ("3.13.1t", "python==3.13.1"),
    ],
)
def test_solve_python_match_spec(mocker, python, expected):
    solver = Micromamba()
    mocker.patch.object(solver, "info", return_value={"channels": []})
    call = mocker.patch.object(solver, "_call", return_value={"actions": {"LINK": []}})

    assert solver.solve("test-env", {}, python, "linux-64") == []

    command, environment = call.call_args.args
    assert expected in command
    if python.endswith("t"):
        assert "python-freethreading" in command
    assert environment["CONDA_SUBDIR"] == "linux-64"
