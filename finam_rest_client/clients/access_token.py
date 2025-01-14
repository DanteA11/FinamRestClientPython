"""Логика работы с токеном."""

import logging

from aiohttp import ClientSession

from finam_rest_client.exceptions import AuthenticationException

from .base import BaseObjClient


class AccessToken(BaseObjClient):
    """Класс для работы с токеном доступа."""

    path = "/public/api/v1/access-tokens/check"
    method = "get"
    logger = logging.getLogger("finam_rest_client.AccessToken")

    async def check_token(self):
        """
        Асинхронный метод, проверяет токен на валидность.

        Для проверки создается новый, отдельный экземпляр сессии.

        :raise AuthenticationError: Если токен не прошел проверку.
        """
        self.logger.debug("Запущена проверка токена.")
        async with ClientSession(
            base_url=self.client.url, headers=self.client.headers
        ) as session:
            response, ok = await self.client.execute_request(
                self.method, self.path, another_session=session
            )
            if not ok:
                self.logger.warning("Токен провалил проверку.")
                raise AuthenticationException()
            self.logger.debug("Токен прошел проверку.")
