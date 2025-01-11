from datetime import date, datetime, timedelta
from random import randint

import pytest

from finam_rest_client.models.response_models import (
    DayCandles,
    IntraDayCandles,
    Orders,
    Portfolio,
    Securities,
    Stops,
)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "code, time_frame",
    (
        ("SBER", "D1"),
        ("SBER", "W1"),
        ("VTBR", "D1"),
        ("VTBR", "W1"),
    ),
)
async def test_get_day_candles(client, code, time_frame):
    random_date = date.today() - timedelta(days=randint(1, 20))
    count = randint(1, 20)
    if randint(0, 1):
        from_ = None
        to = random_date
    else:
        from_ = random_date
        to = None
    result = await client.get_candles(
        security_board="TQBR",
        security_code=code,
        time_frame=time_frame,
        count=count,
        from_=from_,
        to=to,
    )
    assert result.data is not None
    assert result.error is None
    assert len(result.data.candles) <= count
    assert isinstance(result, DayCandles)


@pytest.mark.anyio
async def test_get_day_candles_with_bad_code(client):
    random_date = date.today() - timedelta(days=randint(1, 20))
    count = randint(1, 20)
    if randint(0, 1):
        from_ = None
        to = random_date
    else:
        from_ = random_date
        to = None
    result = await client.get_candles(
        security_board="TQBR",
        security_code="code",
        time_frame="D1",
        count=count,
        from_=from_,
        to=to,
    )
    assert result.data is None
    assert result.error is not None
    assert isinstance(result, DayCandles)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "code, time_frame",
    (
        ("SBER", "M1"),
        ("SBER", "M5"),
        ("VTBR", "M15"),
        ("VTBR", "H1"),
    ),
)
async def test_get_intraday_candles(client, code, time_frame):
    random_datetime = datetime.now() - timedelta(hours=randint(1, 20))
    count = randint(1, 20)
    if randint(0, 1):
        from_ = None
        to = random_datetime
    else:
        from_ = random_datetime
        to = None
    result = await client.get_candles(
        security_board="TQBR",
        security_code=code,
        time_frame=time_frame,
        count=count,
        from_=from_,
        to=to,
    )
    assert result.data is not None
    assert result.error is None
    assert len(result.data.candles) <= count
    assert isinstance(result, IntraDayCandles)


@pytest.mark.anyio
async def test_get_portfolio(client, client_id):
    result = await client.get_portfolio(client_id=client_id)
    assert result.error is None
    assert result.data.client_id == client_id
    assert isinstance(result, Portfolio)


@pytest.mark.anyio
async def test_get_portfolio_without_client_id(client):
    result = await client.get_portfolio(client_id="")
    assert result.error is not None
    assert result.data is None
    assert result.error.data.get("ClientId") is not None
    assert isinstance(result, Portfolio)


@pytest.mark.anyio
async def test_get_portfolio_with_bad_client_id(client):
    result = await client.get_portfolio(client_id="asd")
    assert result.data is None
    assert result.error is not None
    assert isinstance(result, Portfolio)


@pytest.mark.anyio
async def test_get_orders(client, client_id):
    result = await client.get_orders(client_id=client_id)
    assert result.error is None
    assert result.data is not None
    assert result.data.client_id == client_id
    assert isinstance(result.data.orders, list)
    assert isinstance(result, Orders)


@pytest.mark.anyio
async def test_get_orders_with_bad_client_id(client):
    result = await client.get_orders(client_id="client_id")
    assert result.error is not None
    assert result.data is None
    assert isinstance(result, Orders)


@pytest.mark.anyio
async def test_get_stops(client, client_id):
    result = await client.get_stops(client_id=client_id)
    assert result.error is None
    assert result.data is not None
    assert result.data.client_id == client_id
    assert isinstance(result.data.stops, list)
    assert isinstance(result, Stops)


@pytest.mark.anyio
async def test_get_stops_with_bad_client_id(client):
    result = await client.get_stops(client_id="client_id")
    assert result.error is not None
    assert result.data is None
    assert isinstance(result, Stops)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "code",
    ("SBER", "VTBR", "NVTK"),
)
async def test_get_securities_from_db(client, code):
    result = await client.get_securities(seccode=code)
    assert result.data is not None
    assert result.error is None
    assert isinstance(result.data.securities, list)
    assert isinstance(result, Securities)


@pytest.mark.anyio
async def test_get_securities_from_api(client):
    result = await client.get_securities(seccode="GAZP", from_api=True)
    assert result.data is not None
    assert result.error is None
    assert isinstance(result.data.securities, list)
    assert isinstance(result, Securities)


@pytest.mark.anyio
async def test_get_many_request_securities_from_api(client):
    await client.get_securities(seccode="qwerty")
    result = await client.get_securities(seccode="qwerty")
    assert result.data is None
    assert result.error is not None
    assert isinstance(result, Securities)
