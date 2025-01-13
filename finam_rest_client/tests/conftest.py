import pytest

from finam_rest_client.clients import FinamRestClient

token = ""
c_id = ""
with_db = False

if not token or not c_id:
    pytest.exit(
        "Не установлен token или client_id. Установите их в файле conftest.py"
    )


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with FinamRestClient(token, with_db=with_db) as client:
        yield client


@pytest.fixture(scope="session")
async def client_id():
    return c_id
