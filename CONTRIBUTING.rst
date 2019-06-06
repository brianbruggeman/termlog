============
Contributing
============

Please feel free to submit issues and (even better!) pull requests.

Note that we use:

* isort: for styling the top imports
* flake8: for general linting
* mypy: for type linting
* pytest: for tests
* coverage: for test path coverage


Testing
=======

For a quick-start and testing while development:

.. code-block:: bash

    pip install -e .[test]
    pytest --lf -vv -x


For a full release or before a pull request:

.. code-block:: bash

    pytest --isort --flake8 --mypy --cache-clear -n 8 -vv -r a --cov --cov-report=term-missing --cov-report=term:skip-covered --cov-fail-under=75
