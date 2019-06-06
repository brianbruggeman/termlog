"""Pushes a new package to pypi
"""
import shutil
import sys
from pathlib import Path


def clean(force: bool = False):
    """Cleans out folders under repository

    Args:
        force: remove despite any conflicts

    """
    repo_path = Path(__file__).parent.parent
    available = list(repo_path.glob('**/*'))
    files = [p for p in available if p.is_file()]
    folders = [p for p in available if p.is_dir()]
    removables = [
        'build', 'dist',
        '*.egg-info', '*.egg', '.eggs',
        '.coverage.*', '.coverage',
        '__pycache__',
        '.mypy_cache', '.pytest_cache',
        '*.py[co]', 'tmp*',
        ]
    for path in files:
        for removable in removables:
            if path.match(removable):
                path.unlink()
                break
    for path in folders:
        for removable in removables:
            if path.match(removable):
                if force:
                    shutil.rmtree(f'{path}')
                else:
                    try:
                        path.rmdir()
                    except OSError:
                        print(f'WARNING: Not empty/removed: {path}', file=sys.stderr)
                        break


if __name__ == '__main__':
    import click

    @click.command()
    def cli():
        clean()
