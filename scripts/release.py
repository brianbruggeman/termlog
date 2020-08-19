"""Pushes a new package to pypi
"""
import shlex
from pathlib import Path
from subprocess import CalledProcessError, run

import click

from termlog.__metadata__ import package_metadata


def push_pypi(pypi_url: str = "pypi-test"):
    dist_path = Path(__file__).parent.parent / "dist"
    current_version = package_metadata.version
    commands = []
    for file in dist_path.glob("*"):
        if current_version in file.name:
            commands.append(f"twine upload --verbose -r {pypi_url} dist/{file.relative_to(dist_path)}")
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
    @click.option("-d", "--devpi", is_flag=True, show_default=True, help="Push to devpi")
    @click.option("-e", "--ecr", is_flag=True, show_default=True, help="Push to ecr")
    @click.option("-h", "--docker-hub", is_flag=True, show_default=True, help="Push to docker-hub")
    @click.option("-p", "--pypi", is_flag=True, show_default=True, help="Push to pypi")
    @click.option("-u", "--pypi-url", metavar="URL", default="pypi-test", show_default=True, help="URL to pypi upload location")
    def cli(devpi, ecr, docker_hub, pypi, pypi_url):
        if pypi:
            push_pypi(pypi_url=pypi_url)
        # TODO:
        # if devpi:
        #     push_devpi()
        # if ecr:
        #     push_ecr()
        # if docker_hub:
        #     push_docker_hub()

    cli()
