"""This is just a simple benchmarking mechanism to determine
timings for different options.
"""
import time
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from typing import Callable, List, Tuple

from termlog import echo, green, magenta, set_config

set_config(timestamp=False)


@dataclass
class Duration:
    """Holds a duration

    Attributes:
        seconds: the original duration
        unit: the duration to use or the duration calculated
        duration: calculated duration in unites

    """
    seconds: float = field(default=0.0, repr=False, init=True)
    unit: str = ''
    duration: float = field(default=0.0, repr=True, init=False)

    def __post_init__(self):
        duration = self.seconds
        current_unit = 'sec'
        if duration < 1.0:
            for current_unit in ['sec', 'msec', 'usec', 'nsec']:
                if duration < 1.0:
                    duration = duration * 1000
                else:
                    break
        elif duration > 60.0:
            for current_unit, interval in {'sec': 60, 'min': 60, 'hour': 24, 'days': 7}.items():
                if duration >= interval:
                    duration = duration / interval
                else:
                    break
        self.duration = duration
        self.unit = current_unit

    def __str__(self):
        return f'{self.duration:7.2f} {self.unit}'


@dataclass
class TimedExecutionBlock:
    """Context manager for profiling the cpu time of a block of code

    Times a ``with`` block and provides elapsed time.

    """
    start: float = 0.0
    end: float = 0.0

    @property
    def now(self) -> Callable:
        return time.time

    @property
    def seconds(self) -> float:
        """Elapsed seconds time property.

        Returns:
            float: elapsed time in seconds
        """
        end = self.end or self.now()
        return end - self.start

    @property
    def human(self) -> Tuple[float, str]:
        duration = Duration(self.seconds)
        return duration.duration, duration.unit

    def __str__(self):
        duration, unit = self.human
        return f'{duration:0.2f} {unit}'

    def __enter__(self):
        self.start = self.now()
        return self

    def __exit__(self, _type, _value, _traceback):
        self.end = self.now()


def benchmark_all(count: int = 1000):
    readme = (Path(__file__).parent.parent / 'README.rst').read_text('utf-8')
    data = [
        'Hello, World!',
        'Greetings!',
        readme,
        ]
    benchmark_print(data, count=count)
    benchmark_echo(data, count=count)


def benchmark_print(data: List[str], count: int = 1000):
    with TimedExecutionBlock() as time:
        for run in range(count):
            for line in data:
                print(line, file=StringIO())
        duration, unit = time.human
        echo(f'`{green("print")}` took {magenta(f"{duration:.2f}")} {unit}')


def benchmark_echo(data: List[str], count: int = 1000):
    with TimedExecutionBlock() as time:
        for run in range(count):
            for line in data:
                echo(line, file=StringIO())
        duration, unit = time.human
        echo(f' `{green("echo")}` took {magenta(f"{duration:.2f}")} {unit}')


if __name__ == '__main__':
    benchmark_all()
