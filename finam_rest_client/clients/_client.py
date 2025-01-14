import asyncio
import logging
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Self

from finam_rest_client.models.request_models import (
    CancelOrderRequest,
    CancelStopRequest,
    CreateOrderRequest,
    CreateStopRequest,
    DayCandlesRequest,
    GetOrdersRequest,
    GetStopsRequest,
    IntraDayCandlesRequest,
    PortfolioRequest,
    SecuritiesRequest,
)
from finam_rest_client.models.response_models import (
    CancelOrder,
    CancelStop,
    DayCandles,
    IntraDayCandles,
    NewOrder,
    NewStop,
)
from finam_rest_client.models.response_models import Orders as GetOrders
from finam_rest_client.models.response_models import Portfolio as Pf
from finam_rest_client.models.response_models import Securities as Sec
from finam_rest_client.models.response_models import Stops as GetStops

from .access_token import AccessToken
from .base import BaseApiClient
from .candles import Candles
from .orders import Orders, Stops
from .portfolio import Portfolio
from .securities import SecuritiesWithDB, SecuritiesWithoutDB


class FinamRestClient(BaseApiClient):
    """
    Класс для подключения к api.

    Перед использованием важно вызвать метод session_start(),
    а по окончании использования session_end().

    Либо можно воспользоваться асинхронным менеджером контекста.

    :param token: Токен доступа к Api.
    :param with_db: Параметр определяет, стоит ли использовать
      подключение к базе данных для сохранения информации о
      биржевых инструментах. По умолчанию не используются.
    :param drop_all: Опциональный параметр. Указывает нужно ли
      удалять таблицы. Используется только при with_db=True
    :param db_url: Url базы данных для SQLAlchemy.
     Если не установлен, будет использоваться sqlite+aiosqlite.
     Важно добавить асинхронный движок при подключении.
     Например, postgresql+psycopg_async.
     Используется только при with_db=True.
    """

    logger = logging.getLogger("finam_rest_client")
    logger.propagate = False
    __with_db: bool = False

    def __init__(self, token: str, *, with_db: bool = False, **kwargs):
        url = "https://trade-api.finam.ru"
        headers = {"X-Api-Key": token}
        super().__init__(url, headers)

        self._access_token = AccessToken(self)
        self._candles = Candles(self)
        if with_db:
            self.__with_db = with_db
            self._securities = SecuritiesWithDB(self, **kwargs)
        else:
            self._securities = SecuritiesWithoutDB(self)  # type: ignore
        self._portfolio = Portfolio(self)
        self._orders = Orders(self)
        self._stops = Stops(self)

    async def __aenter__(self) -> Self:
        """Вход в менеджер контекста."""
        self.logger.info("Вход в менеджер контекста.")
        await asyncio.gather(
            self.check_token(),
            self._securities.db.start(),
            super().__aenter__(),
        )
        if self.__with_db:
            await self._securities.get_securities()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Выход из менеджера контекста."""
        self.logger.info("Выход из менеджера контекста.")
        await asyncio.gather(
            self._securities.db.stop(),
            super().__aexit__(exc_type, exc_val, exc_tb),
        )

    async def check_token(self) -> None:
        """
        Асинхронный метод, проверяет токен на валидность.

        Для проверки создается новый, отдельный экземпляр сессии.

        :raise AuthenticationError: Если токен не прошел проверку.
        """
        self.logger.info("Запущена проверка токена.")
        await self._access_token.check_token()
        self.logger.info("Токен валиден.")

    async def get_candles(
        self,
        security_code: str,
        security_board: str,
        time_frame: Literal["M1", "M5", "M15", "H1", "D1", "W1"],
        from_: date | datetime | None = None,
        to: date | datetime | None = None,
        count: int | None = None,
    ) -> DayCandles | IntraDayCandles:
        """
        Получение свечей.

        :param security_code: Код инструмента;
        :param security_board: код площадки;
        :param time_frame: тайм-фрейм;
        :param from_: начало интервала, datetime для внутридневных,
          для остальных date;
        :param to: конец интервала, datetime для внутридневных,
          для остальных date;
        :param count: количество свечей.

        :return: Свечи.
        """
        self.logger.info(
            "Метод запущен с параметрами: security_code=%s, "
            "security_board=%s, time_frame=%s, from_=%s, to=%s, count=%s.",
            security_code,
            security_board,
            time_frame,
            from_,
            to,
            count,
        )
        params = dict(
            security_board=security_board,
            security_code=security_code,
            count=count,
            time_frame=time_frame,
            from_=from_,
            to=to,
        )
        if time_frame in ("D1", "W1"):
            model_type = DayCandlesRequest
            func = self._candles.get_day_candles
        else:
            model_type = IntraDayCandlesRequest  # type: ignore
            func = self._candles.get_intraday_candles  # type: ignore
        model = model_type.model_validate(params)
        result = await func(req_candles=model)
        self.logger.info("Получены свечи: %s.", result)
        return result

    async def get_securities(
        self,
        board: str | None = None,
        seccode: str | None = None,
        *,
        from_api: bool = False,
    ) -> Sec:
        """
        Получение списка инструментов.

        :param board: Режим торгов (необязательное поле для фильтрации);
        :param seccode: тикер инструмента (необязательное поле для фильтрации).
        :param from_api: Запросить данные из api. Если False,
          то данные сперва запрашиваются в БД. Только при with_db=True.

        :return: Модель инструментов.
        """
        self.logger.info(
            "Метод запущен с параметрами: board=%s, seccode=%s, from_api=%s.",
            board,
            seccode,
            from_api,
        )
        model = SecuritiesRequest(board=board, seccode=seccode)
        result = await self._securities.get_securities(
            req_securities=model, from_api=from_api
        )
        self.logger.info("Метод вернул: %s.", result)
        return result

    async def get_portfolio(
        self,
        client_id: str,
        include_currencies: bool = True,
        include_money: bool = True,
        include_positions: bool = True,
        include_max_buy_sell: bool = True,
    ) -> Pf:
        """
        Получение портфеля.

        :param client_id: Торговый код клиента;
        :param include_currencies: запросить информацию по
          валютам портфеля;
        :param include_money: запросить информацию по денежным
          позициям портфеля;
        :param include_positions: запросить информацию по позициям портфеля;
        :param include_max_buy_sell: запросить информацию о максимальном
          доступном объеме на покупку/продажу.

        :return: Модель портфеля.
        """
        self.logger.info(
            "Метод запущен с параметрами: client_id=%s, "
            "include_currencies=%s, include_money=%s, "
            "include_positions=%s, include_max_buy_sell=%s.",
            client_id,
            include_currencies,
            include_money,
            include_positions,
            include_max_buy_sell,
        )
        model = PortfolioRequest(
            client_id=client_id,
            include_currencies=include_currencies,
            include_money=include_money,
            include_positions=include_positions,
            include_max_buy_sell=include_max_buy_sell,
        )
        result = await self._portfolio.get_portfolio(req_portfolio=model)
        self.logger.info("Получена информация о портфеле: %s.", result)
        return result

    async def get_orders(
        self,
        client_id: str,
        include_matched: bool = True,
        include_canceled: bool = True,
        include_active: bool = True,
    ) -> GetOrders:
        """
        Получение списка ордеров.

        :param client_id: Торговый код клиента;
        :param include_matched: вернуть исполненные заявки;
        :param include_canceled: вернуть отмененные заявки;
        :param include_active: вернуть активные заявки.

        :return: Модель Ответа на запрос списка ордеров.
        """
        self.logger.info(
            "Метод запущен с параметрами: client_id=%s, "
            "include_matched=%s, include_canceled=%s, include_active=%s.",
            client_id,
            include_matched,
            include_canceled,
            include_active,
        )
        model = GetOrdersRequest(
            client_id=client_id,
            include_canceled=include_canceled,
            include_active=include_active,
            include_matched=include_matched,
        )
        result = await self._orders.get_orders(req_orders=model)
        self.logger.info("Получена информация о заявках: %s.", result)
        return result

    async def get_stops(
        self,
        client_id: str,
        include_executed: bool = True,
        include_canceled: bool = True,
        include_active: bool = True,
    ) -> GetStops:
        """
        Получение списка стоп-ордеров.

        :param client_id: Торговый код клиента;
        :param include_executed: вернуть исполненные стоп-заявки;
        :param include_canceled: вернуть отмененные заявки;
        :param include_active: вернуть активные заявки.

        :return: Модель ответа на запрос списка стоп-ордеров.
        """
        self.logger.info(
            "Метод запущен с параметрами: client_id=%s, "
            "include_executed=%s, include_canceled=%s, include_active=%s.",
            client_id,
            include_executed,
            include_canceled,
            include_active,
        )
        model = GetStopsRequest(
            client_id=client_id,
            include_canceled=include_canceled,
            include_active=include_active,
            include_executed=include_executed,
        )
        result = await self._stops.get_stops(req_stops=model)
        self.logger.info("Получена информация о стоп-заявках: %s.", result)
        return result

    async def create_order(
        self,
        client_id: str,
        security_board: str,
        security_code: str,
        buy_sell: Literal["Buy", "Sell"],
        quantity: int,
        use_credit: bool = True,
        price: Decimal | str | None = None,
        property: Literal[
            "PutInQueue", "CancelBalance", "ImmOrCancel"
        ] = "PutInQueue",
        use_condition: bool = False,
        condition_type: Literal[
            "Bid",
            "BidOrLast",
            "Ask",
            "AskOrLast",
            "Time",
            "CovDown",
            "CovUp",
            "LastUp",
            "LastDown",
        ] = "Bid",
        condition_price: Decimal | str = "0",
        condition_time: datetime | None = None,
        use_valid_before: bool = False,
        valid_before_type: Literal[
            "TillEndSession", "TillCancelled", "ExactTime"
        ] = "TillEndSession",
        valid_before_time: datetime | None = None,
    ) -> NewOrder:
        """
        Создание нового ордера.

        :param client_id: Торговый код клиента;
        :param security_board: основной режим торгов для инструмента;
        :param security_code: код инструмента;
        :param buy_sell: направление сделки;
        :param quantity: объем заявки в лотах;
        :param use_credit: использование кредита (недоступно для
          срочного рынка);
        :param price: цена исполнения заявки. Для рыночной заявки
          указать значение None (или не передавать это поле).
          Для условной заявки необходимо указать цену исполнения;
        :param property: свойства исполнения частично исполненных заявок;
        :param use_condition: использовать условную заявку;
        :param condition_type: тип условия, которое принимает
          следующие значения:
            - Bid - лучшая цена покупки;
            - BidOrLast- лучшая цена покупки или сделка по заданной
              цене и выше;
            - Ask - лучшая цена продажи;
            - AskOrLast - лучшая цена продажи или сделка по заданной
              цене и ниже;
            - Time - время выставления заявки на Биржу
              (параметр condition_time должен быть установлен);
            - CovDown - обеспеченность ниже заданной;
            - CovUp - обеспеченность выше заданной;
            - LastUp - сделка на рынке по заданной цене или выше;
            - LastDown- сделка на рынке по заданной цене или ниже;
        :param condition_price: значение цены для условия;
        :param condition_time: Время, когда заявка будет отменена на сервере.
          В UTC;
        :param use_valid_before: использовать условия по времени
          действия заявки;
        :param valid_before_type: установка временных рамок действия заявки.
          Принимает значения:
            - TillEndSession - заявка действует до конца сессии;
            - TillCancelled - заявка действует, пока не будет отменена;
            - ExactTime - заявка действует до указанного времени.
             (Параметр valid_before_time должен быть задан.)
        :param valid_before_time: время, когда заявка будет отменена на
          сервере. В UTC.

        :return: Модель ответа на создание нового ордера.
        """
        self.logger.info(
            "Метод запущен с параметрами: client_id=%s, security_board=%s, "
            "security_code=%s, buy_sell=%s, quantity=%s, use_credit=%s, "
            "price=%s, property=%s, use_condition=%s, condition_type=%s, "
            "condition_price=%s, condition_time=%s, use_valid_before=%s, "
            "valid_before_type=%s, valid_before_time=%s.",
            client_id,
            security_board,
            security_code,
            buy_sell,
            quantity,
            use_credit,
            price,
            property,
            use_condition,
            condition_type,
            condition_price,
            condition_time,
            use_valid_before,
            valid_before_type,
            valid_before_time,
        )
        data = dict(
            client_id=client_id,
            security_board=security_board,
            security_code=security_code,
            buy_sell=buy_sell,
            quantity=quantity,
            use_credit=use_credit,
            price=price,
            property=property,
        )
        if use_condition:
            data["condition"] = dict(
                type=condition_type, price=condition_price, time=condition_time
            )
        if use_valid_before:
            data["valid_before"] = dict(
                type=valid_before_type, time=valid_before_time
            )
        model = CreateOrderRequest.model_validate(data)
        result = await self._orders.create_order(req_order=model)
        self.logger.info("Получена информация о новой заявке: %s.", result)
        return result

    async def create_stop(
        self,
        client_id: str,
        security_board: str,
        security_code: str,
        buy_sell: Literal["Buy", "Sell"],
        link_order: int,
        use_stop_loss: bool = False,
        sl_activation_price: Decimal | str = "0",
        sl_price: Decimal | str = "0",
        sl_market_price: bool = True,
        sl_quantity_value: Decimal | str = "1",
        sl_quantity_units: Literal["Percent", "Lots"] = "Lots",
        sl_time: int = 0,
        sl_use_credit: bool = True,
        use_take_profit: bool = False,
        tp_activation_price: Decimal | str = "",
        tp_use_correction_price: bool = False,
        tp_correction_price_value: Decimal | str = "",
        tp_correction_price_units: Literal["Percent", "Pips"] = "Pips",
        tp_use_spread_price: bool = False,
        tp_spread_price_value: Decimal | str = "",
        tp_spread_price_units: Literal["Percent", "Pips"] = "Pips",
        tp_market_price: bool = True,
        tp_quantity_value: Decimal | str = "1",
        tp_quantity_units: Literal["Percent", "Lots"] = "Lots",
        tp_time: int = 0,
        tp_use_credit: bool = True,
        expiration_date: datetime | None = None,
        use_valid_before: bool = False,
        valid_before_type: Literal[
            "TillEndSession", "TillCancelled", "ExactTime"
        ] = "TillEndSession",
        valid_before_time: datetime | None = None,
    ) -> NewStop:
        """
        Создание нового стоп-ордера.

        :param client_id: Торговый код клиента;
        :param security_board: основной режим торгов для инструмента;
        :param security_code: код инструмента;
        :param buy_sell: направление сделки;
        :param link_order: биржевой номер связанной (активной) заявки;
        :param use_stop_loss: создать стоп-лосс;
        :param sl_activation_price: цена активации;
        :param sl_price: цена условной заявки. В случае рыночной
          цены значение должно быть 0;
        :param sl_market_price: значение True указывает на то, что
          необходимо выставить рыночную заявку, иначе выставляется
          условная заявка с ценой price;
        :param sl_quantity_value: значение объема;
        :param sl_quantity_units: единицы измерения;
        :param sl_time: защитное время (секунды);
        :param sl_use_credit: использование кредита (недоступно
          для срочного рынка). Указать значение True, если необходимо
          использовать кредит, иначе False;
        :param use_take_profit: создать тейк-профит;
        :param tp_activation_price: цена активации;
        :param tp_use_correction_price: использовать корректированную цену;
        :param tp_correction_price_value: значение цены;
        :param tp_correction_price_units: единицы измерения;
        :param tp_use_spread_price: использовать защитный спред;
        :param tp_spread_price_value: значение цены;
        :param tp_spread_price_units: единицы измерения;
        :param tp_market_price: значение True указывает на то, что
          необходимо выставить рыночную заявку, иначе выставляется
          условная заявка с ценой price;
        :param tp_quantity_value: значение объема;
        :param tp_quantity_units: единицы измерения;
        :param tp_time: защитное время (секунды);
        :param tp_use_credit: использование кредита (недоступно
          для срочного рынка). Указать значение True, если необходимо
          использовать кредит, иначе False;
        :param expiration_date: дата экспирации заявки FORTS;
        :param use_valid_before: использовать условия по времени
          действия заявки;
        :param valid_before_type: установка временных рамок действия заявки.
          Принимает значения:
            - TillEndSession - заявка действует до конца сессии;
            - TillCancelled - заявка действует, пока не будет отменена;
            - ExactTime - заявка действует до указанного времени.
             (Параметр valid_before_time должен быть задан.)
        :param valid_before_time: время, когда заявка будет отменена на
          сервере. В UTC.

        :return: Модель ответа на создание нового стоп-ордера.
        """
        self.logger.info(
            "Метод запущен с параметрами: client_id=%s, security_board=%s, "
            "security_code=%s, buy_sell=%s, link_order=%s, use_stop_loss=%s, "
            "sl_activation_price=%s, sl_price=%s, sl_market_price=%s, "
            "sl_quantity_value=%s, sl_quantity_units=%s, sl_time=%s, "
            "sl_use_credit=%s, use_take_profit=%s, tp_activation_price=%s, "
            "tp_use_correction_price=%s, tp_correction_price_value=%s, "
            "tp_correction_price_units=%s, tp_use_spread_price=%s, "
            "tp_spread_price_value=%s, tp_spread_price_units=%s, "
            "tp_market_price=%s, tp_quantity_value=%s, tp_quantity_units%s, "
            "tp_time=%s, tp_use_credit=%s, expiration_date=%s, "
            "use_valid_before=%s, valid_before_type=%s valid_before_time=%s.",
            client_id,
            security_board,
            security_code,
            buy_sell,
            link_order,
            use_stop_loss,
            sl_activation_price,
            sl_price,
            sl_market_price,
            sl_quantity_value,
            sl_quantity_units,
            sl_time,
            sl_use_credit,
            use_take_profit,
            tp_activation_price,
            tp_use_correction_price,
            tp_correction_price_value,
            tp_correction_price_units,
            tp_use_spread_price,
            tp_spread_price_value,
            tp_spread_price_units,
            tp_market_price,
            tp_quantity_value,
            tp_quantity_units,
            tp_time,
            tp_use_credit,
            expiration_date,
            use_valid_before,
            valid_before_type,
            valid_before_time,
        )
        data = dict(
            client_id=client_id,
            security_board=security_board,
            security_code=security_code,
            buy_sell=buy_sell,
            expiration_date=expiration_date,
            link_order=link_order,
        )
        if use_stop_loss:
            data["stop_loss"] = dict(  # type: ignore
                activation_price=sl_activation_price,
                price=sl_price,
                market_price=sl_market_price,
                quantity=dict(
                    value=sl_quantity_value, units=sl_quantity_units
                ),
                time=sl_time,
                use_credit=sl_use_credit,
            )
        if use_take_profit:
            data["take_profit"] = take_profit = dict(  # type: ignore
                activation_price=tp_activation_price,
                market_price=tp_market_price,
                quantity=dict(
                    value=tp_quantity_value,
                    units=tp_quantity_units,
                ),
                time=tp_time,
                use_credit=tp_use_credit,
            )
            if tp_use_correction_price:
                take_profit["correction_price"] = dict(
                    value=tp_correction_price_value,
                    units=tp_correction_price_units,
                )
            if tp_use_spread_price:
                take_profit["spread_price"] = dict(
                    value=tp_spread_price_value, units=tp_spread_price_units
                )
        if use_valid_before:
            data["valid_before"] = dict(  # type: ignore
                type=valid_before_type, time=valid_before_time
            )
        model = CreateStopRequest.model_validate(data)
        result = await self._stops.create_stop(req_stop=model)
        self.logger.info(
            "Получена информация о новой стоп-заявке: %s.", result
        )
        return result

    async def cancel_order(
        self, client_id: str, transaction_id: int
    ) -> CancelOrder:
        """
        Отмена ордера.

        Важно: если к лимитной заявке была привязана стоп-заявка,
        то стоп-заявка не будет отменена, пока есть еще
        лимитные заявки по инструменту.

        :param client_id: Торговый код клиента;
        :param transaction_id: идентификатор отменяемой заявки.

        :return: Модель ответа на отмену ордера.
        """
        self.logger.info(
            "Метод запущен с параметрами: client_id=%s, transaction_id=%s.",
            client_id,
            transaction_id,
        )
        model = CancelOrderRequest(
            client_id=client_id, transaction_id=transaction_id
        )
        result = await self._orders.cancel_order(req_order=model)
        self.logger.info("Получена информация об отмене заявки: %s.", result)
        return result

    async def cancel_stop(self, client_id: str, stop_id: int) -> CancelStop:
        """
        Отмена стоп-ордера.

        :param client_id: Торговый код клиента;
        :param stop_id: идентификатор отменяемой стоп-заявки.

        :return: Модель ответа на отмену стоп-ордера.
        """
        self.logger.info(
            "Метод запущен с параметрами: client_id=%s, stop_id=%s.",
            client_id,
            stop_id,
        )
        model = CancelStopRequest(client_id=client_id, stop_id=stop_id)
        result = await self._stops.cancel_stop(req_stop=model)
        self.logger.info(
            "Получена информация об отмене стоп-заявки: %s.", result
        )
        return result
