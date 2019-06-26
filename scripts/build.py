"""Pushes a new package to pypi
"""
import shlex
from subprocess import CalledProcessError, run


def build_image():
    commands = [
        f'docker build .'
        ]
    for command in commands:
        try:
            run(shlex.split(command), check=True)
        except CalledProcessError:
            exit(1)


def build_dist():
    commands = [
        f'python setup.py sdist bdist_wheel',
        ]
    for command in commands:
        try:
            run(shlex.split(command), check=True)
        except CalledProcessError:
            exit(1)


if __name__ == '__main__':
    import click

    @click.command()
    @click.option('-d/-D', '--dist/--no-dist', is_flag=True, default=True, help='Build all distribution files')
    @click.option('-i/-I', '--image/--no-image', is_flag=True, default=True, help='Build image')
    def cli(dist, image):
        if dist:
            build_dist()
        if image:
            build_image()

    cli()
