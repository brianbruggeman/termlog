from pathlib import Path

import toml


def test_matching_versions():
    import termlog

    pyproject_toml_path = Path(__file__).parent.parent / "pyproject.toml"
    assert pyproject_toml_path.exists()

    with pyproject_toml_path.open() as f:
        data = toml.load(f)

    package_version = data.get("tool", {}).get("poetry", {}).get("version", {})
    assert termlog.__version__ == package_version
