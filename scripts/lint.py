"""Pushes a new package to pypi
"""
import shlex
from subprocess import CalledProcessError, run

import click


def lint():
    commands = ["isort -c", "flake8", "mypy termlog"]
    for command in commands:
        try:
            run(shlex.split(command), check=True)
        except CalledProcessError:
            exit(1)
    else:
        if not commands:
            print("ERROR: No files found. Run build first")
            exit(1)


if __name__ == "__main__":

    @click.command()
    def cli():
        lint()

    cli()
