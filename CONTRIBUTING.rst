Contributing
============

You're welcome to come and procrastinate with us :)

This contributing guide is trying to avoid common pitfalls, but the project
development environment is quite common. If it's not your first rodeo, here's a TL;DR

TL;DR
-----

(The following is not meant to be executed as a script)

.. code-block:: console

    $ # Start a postgres Database
    $ docker-compose up -d postgres

    $ # Run the migrations to create procrastinate databases
    $ docker-compose run --rm procrastinate migrate

    $ # Start the procrastinate worker
    $ docker-compose up -d procrastinate

    $ # Display the procrastinate command's help message
    $ docker-compose run --rm procrastinate -h

    $ # Launch tests from the docker container
    $ docker-compose exec procrastinate pytest

Alternatively if you want to develop from your host machine:

.. code-block:: console

    $ # Start a postgres Database
    $ docker-compose up -d postgres

    $ # Install requirements
    $ pip install -r requirements.txt

    $ # Explore tox entrypoints
    $ tox -l

Instructions for using docker-compose
-------------------------------------

Crash course of docker-compose
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Docker-compose_ is a docker tool to run several containers and chain them together to setup your stack. In procrastinate, we setup a postgres database in a container, and a procratinate worker in another container. Here are some of the most useful commands in case you don't know this tool:

.. code-block:: console

    $ # Build or re-build the docker image corresponding to the procrastinate worker
    $ docker-compose build procrastinate

    $ # Start all services in detached mode
    $ docker-compose up -d

    $ # Run another procrastinate command in a new instance of the procrastinate docker image
    $ docker-compose run --rm procrastinate healthchecks

    $ # Execute any bash command in the already running procrastinate docker image
    $ docker-compose exec procrastinate echo "Hello world"

    $ # If you changed some code on procrastinate and need to restart the worker
    $ docker-compose restart procrastinate

.. _Docker-compose: https://docs.docker.com/compose/

Create your development database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The development database can be launched using docker with a single command.
The PostgreSQL database we used is a fresh standard out-of-the-box database
on the latest stable version.

.. code-block:: console

    $ docker-compose up -d

The first time, you additionally need to create procrastinate databases.

.. code-block:: console

    $ docker-compose run --rm procrastinate migrate

Try our demo
^^^^^^^^^^^^

You can see the docker worker with:

.. code-block:: console

    $ docker-compose logs -ft procrastinate

Schedule some tasks with:

.. code-block:: console

    $ docker-compose run --rm procrastinate defer procrastinate_demo.tasks.sum '{"a":3, "b": 5}'

Or

.. code-block:: console

    $ docker-compose exec procrastinate python -m procrastinate_demo

Run the project automated tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Within docker container:

.. code-block:: console

    $ docker-compose exec procrastinate pytest  # Test the code using the docker image

To look at coverage in the browser after launching the tests, open the generated webpage in the repository:

.. code-block:: console

    $ python -m webbrowser htmlcov/index.html

Build the documentation
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    $ docker-compose exec procrastinate tox -e docs
    $ python -m webbrowser docs/_build/html/index.html

Developing outside of docker-compose
------------------------------------

If you prefer to work directly from your host machine, you can use virtualenv or tox to setup a development environment. Note that you need to have a running postgresql database, either on your machine, by using a docker image of postgresql, or by reusing only the postgresql part of the docker-compose

.. code-block:: console

    $ docker-compose start postgres

The `export` command below will be necessary whenever you want to interact with
the database (using the project locally, launching tests, ...).
These are standard ``libpq`` environment variables, and the values used below correspond
to the docker setup. Feel free to adjust them as necessary.

.. code-block:: console

    $ export PGDATABASE=procrastinate PGHOST=localhost PGUSER=postgres

Set up your development environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't plan to run the code interactively and just want to run tests,
linting and build the doc, you'll just need ``tox``. You can install it
for your user:

.. code-block:: console

    $ pip install --user tox

In order for this to work, you'll need to make sure your python user install binary
directory is included in your shell's ``PATH``. One way of doing that is to add
a line in your ``~/.profile`` (or ``~/.zprofile`` for ``zsh``). The following command
will output the line to write in that file:

.. code-block:: console

    echo "export PATH=$(python3 -c "import site; print(site.USER_BASE)")/bin:"'$PATH'

If you plan to launch the project locally, install the package itself with development
dependencies in a virtual environment:

.. code-block:: console

    $ python3 -m venv .venv
    $ source .venv/bin/activate

You can check that your Python environment is properly activated:

.. code-block:: console

    (venv) $ which python
    /path/to/current/folder/.venv/bin/python

Install local dependencies:

.. code-block:: console

    (venv) $ pip install -r requirements.txt

Run the project automated tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With a running database:

.. code-block:: console

    (venv) $ pytest  # Test the code with the current interpreter

Or

.. code-block:: console

    $ tox  # Run all the checks for all the interpreters

If you're not familiar with Pytest_, do yourself a treat and look into this fabulous
tool.

.. _Pytest: https://docs.pytest.org/en/latest/

If you don't know Tox_, have a look at their documentation, it's a very nice tool too.

.. _Tox: https://tox.readthedocs.io/en/latest/

To look at coverage in the browser after launching the tests, use:

.. code-block:: console

    $ python -m webbrowser htmlcov/index.html

Keep your code clean
^^^^^^^^^^^^^^^^^^^^

Before committing:

.. code-block:: console

    $ tox -e format

If you've committed already, you can do a "Oops lint" commit, but the best is to run:

.. code-block:: console

    $ git rebase -i --exec 'tox -e format' origin/master

This will run all code formatters on each commits, so that they're clean.
If you've never done an `interactive rebase`_ before, it may seem complicated, so you
don't have to, but... Learn it, it's really cool !

.. _`interactive rebase`: https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History

You can also install a `pre-commit`
hook which makes sure that all your commits are created clean:

.. code-block:: console

    cat > .git/hooks/pre-commit <<EOF
    #!/bin/bash -e
    exec ./pre-commit-hook
    EOF
    chmod +x .git/hooks/pre-commit

If ``tox`` is installed inside your ``virtualenv``, you may want to activate the
``virtualenv`` in ``.git/hooks/pre-commit``:

.. code-block:: bash

    #!/bin/bash -e
    source /path/to/venv/bin/activate
    exec ./pre-commit-hook

This will keep you from creating a commit if there's a linting problem.

Build the documentation
^^^^^^^^^^^^^^^^^^^^^^^

Without spell checking:

.. code-block:: console

    $ tox -e docs
    $ python -m webbrowser docs/_build/html/index.html

Run spell checking on the documentation:

.. code-block:: console

    $ sudo apt install enchant
    $ tox -e docs-spelling

Because of outdated software and version incompatibilities, spell checking is not
checked in the CI, and we don't require people to run it in their PR. Though, it's
always a nice thing to do. Feel free to include any spell fix in your PR, even if it's
not related to your PR (but please put it in a dedicated commit).

If you need to add words to the spell checking dictionary, it's in
``docs/spelling_wordlist.txt``. Make sure the file is alphabetically sorted!

Wait, there are ``async`` and ``await`` keywords everywhere!?
-------------------------------------------------------------

Yes, in order to provide both a synchronous **and** asynchronous API, Procrastinate
needs to be asynchronous at core.

We're using a trick to avoid implementing two almost identical APIs for synchronous
and asynchronous usage. Find out more in the documentation, in the Discussions
section. If you need information on how to work with asynchronous Python, check out:

- The official documentation: https://docs.python.org/3/library/asyncio.html
- A more accessible guide by Brad Solomon: https://realpython.com/async-io-python/
