"""Pushes a new package to pypi
"""
from subprocess import CalledProcessError, run

import click


def run_test(release: bool = False, coverage_fail_threshold=75):
    command = ['pytest']
    if release:
        command.extend([
            '--cache-clear',
            '-vv',
            '-r a',
            '--cov',
            '--cov-report=term-missing',
            '--cov-report=term:skip-covered',
            f'--cov-fail-under={coverage_fail_threshold}'
            ])

    try:
        run(command, check=True)
    except CalledProcessError:
        exit(1)


if __name__ == '__main__':
    @click.command()
    @click.option('-r', '--release', help='Run as a release')
    @click.option('-t', '--threshold', help='Coverage fail threshold')
    def cli(release, threshold):
        run_test(release=release, coverage_fail_threshold=threshold)

    cli()
