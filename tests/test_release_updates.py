"""
These tests validate that all of the standard release updates are
present since pyproject.toml inherently makes the python project WET.

"""
from pathlib import Path

import toml

repo_path = Path(__file__).parent.parent

def test_version_in_changes():
    """Validates that some release notes have been added to
    CHANGES.rst

    """
    import termlog

    changes_path = repo_path / "CHANGES.rst"
    found = False
    for line in changes_path.read_text("utf-8").split("\n"):
        if line.startswith(termlog.__version__):
            found = True

    assert found is True


def test_matching_versions():
    """Validates that the version in pyproject.toml matches the version
    in termlog/__init__.py

    """
    import termlog

    pyproject_toml_path = repo_path / "pyproject.toml"
    assert pyproject_toml_path.exists()

    with pyproject_toml_path.open() as f:
        data = toml.load(f)

    package_version = data.get("tool", {}).get("poetry", {}).get("version", {})
    assert termlog.__version__ == package_version
