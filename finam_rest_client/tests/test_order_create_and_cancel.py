import asyncio
from datetime import datetime

import pytest

from finam_rest_client.models.common_types import OrderStatus
from finam_rest_client.models.response_models import (
    CancelOrder,
    IntraDayCandles,
    NewOrder,
    Orders,
)


@pytest.mark.anyio
async def test_create_conditional_order_buy(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert isinstance(orders, Orders)
    amount = len(orders.data.orders)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = str(round(high_price * 1.03, high_price_finam.scale))

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Buy",
        quantity=1,
        use_condition=True,
        condition_type="LastUp",
        condition_price=price,
    )
    assert isinstance(new_order, NewOrder)
    assert new_order.data is not None
    assert new_order.error is None
    assert new_order.data.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    assert len(orders.data.orders) == amount + 1


@pytest.mark.anyio
async def test_cancel_conditional_order_buy(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert isinstance(orders, Orders)
    amount = len(orders.data.orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    length = len(idx)
    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = str(round(high_price * 1.03, high_price_finam.scale))

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Buy",
        quantity=1,
        use_condition=True,
        condition_type="LastUp",
        condition_price=price,
    )
    assert isinstance(new_order, NewOrder)
    assert new_order.data is not None
    assert new_order.error is None
    assert new_order.data.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    assert len(orders.data.orders) == amount + 1

    result = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.data.transaction_id
    )
    assert isinstance(result, CancelOrder)
    assert result.data is not None
    assert result.error is None
    assert result.data.client_id == client_id
    assert result.data.transaction_id == new_order.data.transaction_id

    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    assert len(idx) == length


@pytest.mark.anyio
async def test_create_limit_order_buy(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert isinstance(orders, Orders)
    amount = len(orders.data.orders)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = str(round(high_price * 0.97, high_price_finam.scale))

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Buy",
        quantity=1,
        price=price,
    )
    assert isinstance(new_order, NewOrder)
    assert new_order.data is not None
    assert new_order.error is None
    assert new_order.data.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    assert len(orders.data.orders) == amount + 1


@pytest.mark.anyio
async def test_cancel_limit_order_buy(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert isinstance(orders, Orders)
    amount = len(orders.data.orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    length = len(idx)
    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = str(round(high_price * 0.97, high_price_finam.scale))

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Buy",
        quantity=1,
        price=price,
    )
    assert isinstance(new_order, NewOrder)
    assert new_order.data is not None
    assert new_order.error is None
    assert new_order.data.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    assert len(orders.data.orders) == amount + 1

    result = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.data.transaction_id
    )
    assert isinstance(result, CancelOrder)
    assert result.data is not None
    assert result.error is None
    assert result.data.client_id == client_id
    assert result.data.transaction_id == new_order.data.transaction_id

    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    assert len(idx) == length


@pytest.mark.anyio
async def test_create_conditional_order_sell(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert isinstance(orders, Orders)
    amount = len(orders.data.orders)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = str(round(high_price * 0.97, high_price_finam.scale))

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Sell",
        quantity=1,
        use_condition=True,
        condition_type="LastDown",
        condition_price=price,
    )
    assert isinstance(new_order, NewOrder)
    assert new_order.data is not None
    assert new_order.error is None
    assert new_order.data.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    assert len(orders.data.orders) == amount + 1


@pytest.mark.anyio
async def test_cancel_conditional_order_sell(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert isinstance(orders, Orders)
    amount = len(orders.data.orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    length = len(idx)
    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = str(round(high_price * 0.97, high_price_finam.scale))
    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Sell",
        quantity=1,
        use_condition=True,
        condition_type="LastDown",
        condition_price=price,
    )
    assert isinstance(new_order, NewOrder)
    assert new_order.data is not None
    assert new_order.error is None
    assert new_order.data.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    assert len(orders.data.orders) == amount + 1

    result = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.data.transaction_id
    )
    assert isinstance(result, CancelOrder)
    assert result.data is not None
    assert result.error is None
    assert result.data.client_id == client_id
    assert result.data.transaction_id == new_order.data.transaction_id

    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    assert len(idx) == length


@pytest.mark.anyio
async def test_create_limit_order_sell(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert isinstance(orders, Orders)
    amount = len(orders.data.orders)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = str(round(high_price * 1.03, high_price_finam.scale))

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Sell",
        quantity=1,
        price=price,
    )
    assert isinstance(new_order, NewOrder)
    assert new_order.data is not None
    assert new_order.error is None
    assert new_order.data.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    assert len(orders.data.orders) == amount + 1


@pytest.mark.anyio
async def test_cancel_limit_order_sell(client, client_id):
    orders_task = asyncio.create_task(client.get_orders(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )
    orders = await orders_task
    assert isinstance(orders, Orders)
    amount = len(orders.data.orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    length = len(idx)
    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price = str(round(high_price * 1.03, high_price_finam.scale))

    new_order = await client.create_order(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Sell",
        quantity=1,
        price=price,
    )
    assert isinstance(new_order, NewOrder)
    assert new_order.data is not None
    assert new_order.error is None
    assert new_order.data.client_id == client_id
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    assert len(orders.data.orders) == amount + 1

    result = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.data.transaction_id
    )
    assert isinstance(result, CancelOrder)
    assert result.data is not None
    assert result.error is None
    assert result.data.client_id == client_id
    assert result.data.transaction_id == new_order.data.transaction_id

    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    assert len(idx) == length


@pytest.mark.anyio
async def test_cancel_all_orders(client, client_id):
    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    tasks = []
    for id_ in idx:
        tasks.append(
            client.cancel_order(client_id=client_id, transaction_id=id_)
        )
    results = await asyncio.gather(*tasks)
    for result in results:
        assert isinstance(result, CancelOrder)
        assert result.data is not None
        assert result.error is None
        assert result.data.client_id == client_id
        assert result.data.transaction_id in idx
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(client_id=client_id)
    assert isinstance(orders, Orders)
    idx = [
        order.transaction_id
        for order in orders.data.orders
        if order.status == OrderStatus.active
    ]
    assert len(idx) == 0
