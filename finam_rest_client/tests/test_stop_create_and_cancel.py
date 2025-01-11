import asyncio
from datetime import datetime

import pytest

from finam_rest_client.models.response_models import (
    CancelStop,
    IntraDayCandles,
    NewOrder,
    Stops,
)


@pytest.mark.anyio
async def test_create_stop_loss_sell(client, client_id):
    stops_task = asyncio.create_task(client.get_stops(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert isinstance(stops, Stops)
    amount = len(stops.data.stops)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price_num = round(high_price * 0.97, high_price_finam.scale)
    price = str(price_num)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders.data.orders
    order_no = orders.data.orders[0].order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_act_price = str(round(price_num * 0.99, high_price_finam.scale))
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Sell",
        link_order=order_no,
        use_stop_loss=True,
        sl_activation_price=stop_act_price,
        sl_market_price=False,
        use_valid_before=True,
        valid_before_type="TillEndSession",
    )
    assert new_stop.data is not None
    assert new_stop.error is None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(client_id=client_id)
    assert isinstance(stops, Stops)
    assert len(stops.data.stops) == amount + 1


@pytest.mark.anyio
async def test_create_stop_loss_buy(client, client_id):
    stops_task = asyncio.create_task(client.get_stops(client_id=client_id))
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert isinstance(stops, Stops)
    amount = len(stops.data.stops)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price_num = round(high_price * 1.03, high_price_finam.scale)
    price = str(price_num)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders.data.orders
    order_no = orders.data.orders[0].order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_act_price = str(round(price_num * 1.01, high_price_finam.scale))
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Buy",
        link_order=order_no,
        use_stop_loss=True,
        sl_activation_price=stop_act_price,
        sl_market_price=False,
        use_valid_before=True,
        valid_before_type="TillEndSession",
    )
    assert new_stop.data is not None
    assert new_stop.error is None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(client_id=client_id)
    assert isinstance(stops, Stops)
    assert len(stops.data.stops) == amount + 1


@pytest.mark.anyio
async def test_cancel_stop_order(client, client_id):
    stops_task = asyncio.create_task(
        client.get_stops(
            client_id=client_id, include_executed=False, include_canceled=False
        )
    )
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert isinstance(stops, Stops)
    amount = len(stops.data.stops)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price_num = round(high_price * 0.97, high_price_finam.scale)
    price = str(price_num)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders.data.orders
    amount_orders = len(orders.data.orders)
    order_no = orders.data.orders[0].order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_act_price = str(round(price_num * 0.99, high_price_finam.scale))
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Sell",
        link_order=order_no,
        use_stop_loss=True,
        sl_activation_price=stop_act_price,
        sl_market_price=False,
        use_valid_before=True,
        valid_before_type="TillEndSession",
    )
    assert new_stop.data is not None
    assert new_stop.error is None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert isinstance(stops, Stops)
    assert len(stops.data.stops) == amount + 1
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_cancel = await client.cancel_stop(
        client_id=client_id, stop_id=new_stop.data.stop_id
    )
    assert isinstance(stop_cancel, CancelStop)
    assert stop_cancel.error is None
    assert stop_cancel.data is not None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert isinstance(stops, Stops)
    assert len(stops.data.stops) == amount
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert len(orders.data.orders) == amount_orders
    cancel_order = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.data.transaction_id
    )
    assert cancel_order.data is not None
    assert cancel_order.error is None


@pytest.mark.anyio
async def test_create_take_profit_sell(client, client_id):
    stops_task = asyncio.create_task(
        client.get_stops(
            client_id=client_id, include_executed=False, include_canceled=False
        )
    )
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert isinstance(stops, Stops)
    amount = len(stops.data.stops)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price_num = round(high_price * 0.97, high_price_finam.scale)
    price = str(price_num)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders.data.orders
    order_no = orders.data.orders[0].order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    take_act_price = str(round(price_num * 1.01, high_price_finam.scale))
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Sell",
        link_order=order_no,
        use_take_profit=True,
        tp_activation_price=take_act_price,
        tp_market_price=True,
        use_valid_before=True,
        valid_before_type="TillEndSession",
    )
    assert new_stop.data is not None
    assert new_stop.error is None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert isinstance(stops, Stops)
    assert len(stops.data.stops) == amount + 1


@pytest.mark.anyio
async def test_create_take_profit_buy(client, client_id):
    stops_task = asyncio.create_task(
        client.get_stops(
            client_id=client_id, include_executed=False, include_canceled=False
        )
    )
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert isinstance(stops, Stops)
    amount = len(stops.data.stops)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price_num = round(high_price * 1.03, high_price_finam.scale)
    price = str(price_num)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders.data.orders
    order_no = orders.data.orders[0].order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    take_act_price = str(round(price_num * 0.99, high_price_finam.scale))
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Buy",
        link_order=order_no,
        use_take_profit=True,
        tp_activation_price=take_act_price,
        tp_market_price=True,
        use_valid_before=True,
        valid_before_type="TillEndSession",
    )
    assert new_stop.data is not None
    assert new_stop.error is None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert isinstance(stops, Stops)
    assert len(stops.data.stops) == amount + 1


@pytest.mark.anyio
async def test_cancel_order_with_stop_order(client, client_id):
    stops_task = asyncio.create_task(
        client.get_stops(
            client_id=client_id, include_executed=False, include_canceled=False
        )
    )
    candles_task = asyncio.create_task(
        client.get_candles(
            security_board="TQBR",
            security_code="VTBR",
            time_frame="M1",
            count=1,
            to=datetime.now(),
        )
    )

    stops = await stops_task
    assert isinstance(stops, Stops)
    amount = len(stops.data.stops)

    candles = await candles_task
    assert isinstance(candles, IntraDayCandles)
    high_price_finam = candles.data.candles[0].high
    high_price = high_price_finam.num * 10**-high_price_finam.scale
    price_num = round(high_price * 0.97, high_price_finam.scale)
    price = str(price_num)

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

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders.data.orders
    amount_orders = len(orders.data.orders)
    order_no = orders.data.orders[0].order_no
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stop_act_price = str(round(price_num * 0.99, high_price_finam.scale))
    new_stop = await client.create_stop(
        client_id=client_id,
        security_board="TQBR",
        security_code="VTBR",
        buy_sell="Sell",
        link_order=order_no,
        use_stop_loss=True,
        sl_activation_price=stop_act_price,
        sl_market_price=False,
        use_valid_before=True,
        valid_before_type="TillEndSession",
    )
    assert new_stop.data is not None
    assert new_stop.error is None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert isinstance(stops, Stops)
    assert len(stops.data.stops) == amount + 1
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert len(orders.data.orders) == amount_orders
    cancel_order = await client.cancel_order(
        client_id=client_id, transaction_id=new_order.data.transaction_id
    )
    assert cancel_order.data is not None
    assert cancel_order.error is None
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.

    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    idx = [stop.stop_id for stop in stops.data.stops]
    # Стоп остается на месте, пока не будут сняты все ордера по инструменту.
    assert new_stop.data.stop_id in idx


@pytest.mark.anyio
async def test_cancel_all_stops(client, client_id):
    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    idx = [stop.stop_id for stop in stops.data.stops]
    tasks = []
    for id_ in idx:
        tasks.append(client.cancel_stop(client_id=client_id, stop_id=id_))
    results = await asyncio.gather(*tasks)
    for result in results:
        assert isinstance(result, CancelStop)
        assert result.data is not None
        assert result.error is None
        assert result.data.client_id == client_id
        assert result.data.stop_id in idx
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    stops = await client.get_stops(
        client_id=client_id, include_executed=False, include_canceled=False
    )
    assert isinstance(stops, Stops)
    assert stops.data.stops == []


@pytest.mark.anyio
async def test_cancel_all_orders(client, client_id):
    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    idx = [order.transaction_id for order in orders.data.orders]
    tasks = []
    for id_ in idx:
        tasks.append(
            client.cancel_order(client_id=client_id, transaction_id=id_)
        )
    results = await asyncio.gather(*tasks)
    for result in results:
        assert result.data is not None
        assert result.error is None
        assert result.data.client_id == client_id
        assert result.data.transaction_id in idx
    await asyncio.sleep(1)  # Чтобы успела обработаться информация о заявках.
    orders = await client.get_orders(
        client_id=client_id, include_matched=False, include_canceled=False
    )
    assert orders.data.orders == []
