"""Pushes a new package to pypi
"""
import shlex
from pathlib import Path
from subprocess import CalledProcessError, run

from termlog.__metadata__ import package_metadata


def check():
    """Checks if twine """
    dist_path = Path(__file__).parent.parent / "dist"
    current_version = package_metadata.version
    commands = []
    extension = ["*.tar.gz", "*.whl"]
    for file in dist_path.glob("**/*"):
        if any(file.match(ext) for ext in extension):
            if current_version in file.name:
                commands.append(f"twine check dist/{file.relative_to(dist_path)}")
    for command in commands:
        try:
            run(shlex.split(command), check=True)
        except CalledProcessError:
            exit(1)


if __name__ == "__main__":
    import click

    @click.command()
    def cli():
        check()

    cli()
