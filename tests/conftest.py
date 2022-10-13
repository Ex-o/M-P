import psycopg2
import psycopg2.extras
import pytest
from pytest_postgresql import factories

from main import create_app

postgresql_my_proc = factories.postgresql_proc()
psql_proc = factories.postgresql(
    'postgresql_my_proc',
    load=["./database.sql"]
)


@pytest.fixture
def get_db(psql_proc):
    psql_proc = psql_proc.dsn.split(' ')
    creds = {}

    for x in psql_proc:
        k, v = x.split('=')
        creds.update({k: v})
    psql_proc = creds

    conn = psycopg2.connect(
        dbname=psql_proc['dbname'],
        user=psql_proc['user'],
        password=psql_proc['password'],
        host=psql_proc['host'],
        port=psql_proc['port'],
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    yield conn


@pytest.fixture()
def app(get_db):
    app = create_app()
    app.config.update({
        "DSN": get_db.dsn,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
