Use Pum for schema migrations
-----------------------------

When Procrastinate developers make changes to the Procrastinate database schema they
write, so-called, migration scripts.

Here's an example of a migration script:

.. code-block:: sql

    ALTER TABLE procrastinate_jobs ADD COLUMN extra TEXT;

Migration scripts are pure-SQL scripts, so they may be applied to the database using any
PostgreSQL client, including ``psql`` and ``PGAdmin``.

The names of migration script files adhere to a certain pattern, which comes from `Pum`_
(PostgreSQL Updates Manager). This means that Pum may be used to apply Procrastinate
database migrations.

See the `Pum README`_ on GitHub to know how to use Pum. But here is an example, applied
to Procrastinate:

Set baseline:

.. code-block:: console

    pum baseline -p procrastinate -t public.pum -d procrastinate/sql/migrations/ -b 1.2.1

Apply migrations:

.. code-block:: console

    pum upgrade -p procrastinate -t public.pum -d procrastinate/sql/migrations/

.. _`Pum`: https://github.com/opengisch/pum/
.. _`Pum README`: https://github.com/opengisch/pum/blob/master/README.md
