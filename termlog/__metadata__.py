"""This is imported by setup.py and contains all of the information
necessary to run setup.py
"""
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from textwrap import dedent
from typing import Dict, Tuple


# ----------------------------------------------------------------------
# Package Metadata
# ----------------------------------------------------------------------
@dataclass
class PackageMetadata:
    """Package metadata information

    Notes:
        This is used in setup, scripts, cli interface, endpoints, etc.

    Attributes:
        name: name of package
        package_name: import name for package
        title: short human readable title for package
        summary: long human readable title for package
        description: long description for package

        version: semantic version of package
        major: major component of semantic version (X._._)
        minor: minor component of semantic version (_.X._)
        micro: micro component of semantic version (_._.X)
        build: git sha value of build
        release: human friendly release name

        author: package author
        author_email: email for package author

        maintainer: package maintainer
        maintainer_email: package maintainer email

        copyright: copyright years of major work on package
        license: default license for package

        url: location for package repository or documentation

        classifiers:  python trove classifiers
        keywords: keywords for searching for package

    Example:
        The PackageMetadata attributes can be accessed by something
        like the following.

        >>> from termlog.__metadata__ import package_metadata
        >>> package_metadata.name
        termlog

    """
    name: str = 'termlog'
    package_name: str = field(init=False, repr=False, default='')
    title: str = 'Terminal logging built for docker images'
    summary: str = f'A logging '
    description: str = dedent(f"""\
    {summary}

    This code is in Production and provides a micro-service which
    provides content discovery for Audience Similarity, PopularEndpoint
    and PopularityEndpoint.

    The data responses are JSON and enriched with Metadata's data.

    This micro-service relies upon S3 access to authenticate and
    serve Audience Similarity and PopularEndpoint with Metadata.  Additionally,
    this micro-service requires access to PopularityEndpoint's API micro-service.
    """)

    version: str = '1.0.0'
    major: int = field(init=False, repr=False)
    minor: int = field(init=False, repr=False)
    micro: int = field(init=False, repr=False)
    build: str = field(init=False, repr=False)
    release: str = field(init=False, repr=False)

    author: str = 'Brian Bruggeman'
    author_email: str = 'brian.m.bruggeman@gmail.com'

    maintainer: str = 'Brian Bruggeman'
    maintainer_email: str = 'brian.m.bruggeman@gmail.com'

    copyright: str = f'2019'
    license: str = f'MIT'

    url: str = 'https://github.com/brianbruggeman/termlog'

    classifiers: Tuple = (
        'Programming Language :: Python',
        'Natural Language :: English',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Private',  # Prevents uploads to pypi
        )

    keywords: Tuple = (
        'terminal',
        'logger',
        'docker',
        )

    @property
    def setup(self) -> Dict:
        """Returns setup.py friendly fields and values"""
        # see: https://packaging.python.org/specifications/core-metadata/
        required_fields = [
            'metadata_version', 'name', 'version',
            ]
        setup_friendly_fields = required_fields + [
            'platform', 'supported_platform', 'description',
            'description_content_type', 'keywords', 'home_page', 'download_url',
            'author', 'author_email', 'maintainer', 'maintainer_email',
            'license', 'classifier', 'requires_dist', 'requires_python',
            'requires_external', 'project_url', 'provides_extra',
            'provides_dist', 'obsoletes_dist',

            'long_description', 'license', 'version',
            'author', 'author_email', 'maintainer', 'maintainer_email',
            'license', 'url', 'classifiers', 'keywords'
            ]
        data = {}
        for key in self.__annotations__.keys():
            if key in setup_friendly_fields:
                value = getattr(self, key)
                data[key] = value
        data['keywords'] = list(data['keywords'])
        data['classifiers'] = list(data['classifiers'])
        return data

    def __post_init__(self):
        self.package_name = self.name.replace('-', '_')
        self.major, self.minor, self.micro = list(map(int, self.version.split('.')))
        self.build = self._get_build() or ''
        if self.build:
            self.release = f'{self.name} {self.version} [build: {self.build}]'
        else:
            self.release = f'{self.name} {self.version}'

    def _get_build(self):
        # localhost
        git_sha = self._get_git_sha()
        if git_sha:
            return git_sha

        # AWS
        filepath_sha = self._get_filepath_git_sha()
        if filepath_sha:
            return filepath_sha

        # docker
        try:
            # In an effort to clearly identify where we use environment
            # variables, this will use config, but it creates both
            # a circular dependency and causes problems for setup.py
            # which reads this file.  So punt if there are problems
            git_sha_env = os.getenv('CDR_REST_GIT_SHA')
            if git_sha_env:
                return git_sha_env
        except ImportError:
            # Otherwise this will fail during setup.py
            print('Failed to capture build')
            for key, value in sorted(os.environ.items()):
                print(f'{key}: {value}')

    @staticmethod
    def _get_git_sha():
        # In a development enviromment this will have access to git
        #  and it's possible to simply query the last hash value
        git_command = ('git', 'rev-parse', '--short', 'HEAD')
        proc = subprocess.run(git_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0:
            return proc.stdout.decode('utf-8').strip('\n')

    @staticmethod
    def _get_filepath_git_sha():
        # In a production environment, the hash value should be
        #  part of the file path
        for path_fragment in Path(__file__).absolute().parts:
            if not path_fragment or path_fragment == '/':
                continue
            if path_fragment.startswith('termlog-'):
                if 'git.sha' in path_fragment:
                    return path_fragment.split('termlog-')[-1]

    def keys(self):
        yield from self.__annotations__.keys()

    def __getitem__(self, item):
        if item in self.__annotations__.keys():
            value = getattr(self, item)
            return value
        raise AttributeError(f"Could not find {item}")

    def __iter__(self):
        for field in self.__annotations__.keys():
            yield field


package_metadata = PackageMetadata()
