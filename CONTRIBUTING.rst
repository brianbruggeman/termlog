============
Contributing
============

Please feel free to submit issues and (even better!) pull requests.

Note that we use:

* black: for better styling
* isort: for styling the top imports
* mypy: for type linting
* pytest: for tests
* coverage: for test path coverage


Testing
=======

For a quick-start and testing while development:
sort
.. code-block:: bash

    pip install .
    pytest --lf -vv -x


For a full release or before a pull request:

.. code-block:: bash

    pytest --isort --black --mypy --cache-clear -vv -r a --cov --cov-report=term-missing --cov-report=term:skip-covered --cov-fail-under=75
