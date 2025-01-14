"""Логика работы с портфелем."""

import logging

from finam_rest_client.clients.base import BaseObjClient
from finam_rest_client.models.request_models import PortfolioRequest
from finam_rest_client.models.response_models import Portfolio as Pf


class Portfolio(BaseObjClient):
    """Класс для работы с портфелем."""

    path = "/public/api/v1/portfolio"
    method = "get"
    logger = logging.getLogger("finam_rest_client.Portfolio")

    async def get_portfolio(self, req_portfolio: PortfolioRequest) -> Pf:
        """
        Получение портфеля.

        :param req_portfolio: Модель запроса на получение портфеля.

        :return: Модель портфеля.
        """
        self.logger.debug(
            "Метод запущен с параметрами: req_portfolio=%s.", req_portfolio
        )
        data = self.create_data(req_portfolio)
        result = await self._execute_request(
            resp_model=Pf,
            params=data,
            path=self.path,
        )
        self.logger.debug("Получена информация о портфеле: %s.", result)
        return result
