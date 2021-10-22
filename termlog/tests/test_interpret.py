from dataclasses import asdict, dataclass, field
from typing import Set

import pytest


@dataclass
class InterpretTestCase:
    code: str = ""
    expected: Set[str] = field(default_factory=set)

    def __str__(self):
        return " ".join(f"{key}={value}" for key, value in asdict(self).items())


test_cases = [
    InterpretTestCase(),
    InterpretTestCase(
        code="""
        for y in range(10):
            for x in range(10):
                print(f'(y={y}, x={x})')
        """,
        expected={"x", "y"},
    ),
    InterpretTestCase(
        code="""
        def big(foo: str = "") -> str:
            x = foo.join(str(y) for y in range(10))
        """,
        expected={"x", "y", "foo"},
    ),
    InterpretTestCase(
        code="""
        {y for y in range(10)}
        """,
        expected={"y"},
    ),
    InterpretTestCase(
        code="""
        import pdb as p
        """,
        expected={"p"},
    ),
    InterpretTestCase(
        code="""
        x = object()
        try:
            x.y
        except TypeError:
            raise
        except AttributeError as e:
            print(f"badness: {e}")
            raise
        """,
        expected={"x", "e"},
    ),
    InterpretTestCase(
        code="""
        [y for y in range(10)]
        """,
        expected={"y"},
    ),
    InterpretTestCase(
        code="""
        @click.command('ingest')
        @click.option("-A", "--no-aggregation", "no_run_aggregation", is_flag=True, default=False, help="Do not run aggregation")
        @click.option("-c/-C", "--color/--no-color", is_flag=True, default=True if settings.human is True else False, help="Set color on output")
        @click.option("-d/-D", "--debug/--no-debug", is_flag=True, default=settings.debug, help="Sets debug output")
        @click.option("-E", "--no-extract", "no_run_extract", is_flag=True, default=False, help="Do not sync new data from s3")
        @click.option("-j/-J", "--json/--no-json", is_flag=True, default=False if settings.human is True else True, help="Set output format")
        @click.option("-L", "--no-load", "no_run_load", is_flag=True, default=False, help="Do not load database with temp tables")
        @click.option("-S", "--no-swap", "no_run_swap", is_flag=True, default=False, help="Do not swap temp tables with live")
        @click.option("-R", "--no-remove-table", "no_run_remove_table", is_flag=True, default=False, help="Do not remove old temp tables")
        @click.option("-t", "--threads", metavar="COUNT", default=settings.ingestion.threads, show_default=True, type=int, help="threads to use")
        @click.option("-v", "--verbosity", count=True, default=0, show_default=True, help="verbosity level")
        @click.option("-w", "--workers", metavar="COUNT", default=settings.ingestion.workers, show_default=True, type=int, help="cores to use")
        @click.option("--version", is_flag=True, help="show version and quit")
        @click.argument("source_names", default=None, nargs=-1)
        def cli(
                color: Optional[bool] = None,
                debug: Optional[bool] = None,
                json: Optional[bool] = None,
                no_run_aggregation: bool = False,
                no_run_extract: bool = False,
                no_run_remove_table: bool = False,
                no_run_load: bool = False,
                no_run_swap: bool = False,
                source_names: Optional[List[str]] = None,
                threads: int = int(os.cpu_count() or 1) * 5,
                verbosity: int = 0,
                version: bool = False,
                workers: int = int(os.cpu_count() or 1),
                ):
            settings.debug = debug
            termlog.set_palette(termlog.palettes.SolarizedDark)
            termlog.set_config(json=json, color=color)
            sources = match_source_names(source_names or [])
            termlog.echo(f'{termlog.green("ingestion package")}', verbose=verbosity if not version else 1, add_timestamp=False)
            termlog.echo(f'Ingesting: {termlog.cyan(len(sources))} sources', verbose=verbosity if not version else 1)
            if verbosity - 1 > 0 and not version:
                for source_name in sources:
                    termlog.echo(f'Ingesting: {termlog.cyan(source_name)}', verbose=verbosity - 1)
            if not version:
                ingest(sources=sources, run_agg=not no_run_aggregation, run_extract=not no_run_extract, run_load=not no_run_load,
                    run_swap=not no_run_swap, run_table_remove=not no_run_remove_table, threads=threads, verbose=verbosity,
                    workers=workers)
            """,
        expected={
            "sources",
            "no_run_aggregation",
            "no_run_extract",
            "no_run_load",
            "no_run_swap",
            "no_run_remove_table",
            "threads",
            "verbosity",
            "workers",
            "debug",
            "json",
            "color",
            "source_names",
            "source_name",
            "version",
        },
    ),
]


@pytest.mark.parametrize("test_case", test_cases, ids=list(map(str, test_cases)))
def test_extract_fields(test_case):
    from ..interpret import extract_fields

    result = extract_fields(code=test_case.code)
    found_fields = set(result)
    expected = set(test_case.expected)  # because pytest's assert interprets an empty set as a dictionary
    assert found_fields - expected == set()
    assert expected - found_fields == set()
