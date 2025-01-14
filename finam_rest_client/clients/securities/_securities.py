"""Информация о биржевых инструментах."""

import logging

from finam_rest_client.clients.base import BaseObjClient
from finam_rest_client.models.request_models import SecuritiesRequest
from finam_rest_client.models.response_models import Securities as Sec


class Securities(BaseObjClient):
    """Класс для получения данных об инструменте."""

    path = "/public/api/v1/securities"
    method = "get"
    logger = logging.getLogger("finam_rest_api_client.Securities")

    async def get_securities(
        self,
        req_securities: SecuritiesRequest | None = None,
    ) -> Sec:
        """
        Получение списка инструментов.

        :param req_securities: Модель запроса на получение дневных свечей.

        :return: Модель инструментов.
        """
        self.logger.debug(
            "Метод запущен с параметрами: req_securities=%s.", req_securities
        )
        data = None
        if req_securities:
            data = self.create_data(req_securities)
        result = await self._execute_request(
            resp_model=Sec,
            params=data,
            path=self.path,
        )
        self.logger.info("Данные получены из ответа Api.")
        return result
