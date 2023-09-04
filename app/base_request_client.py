import logging
from functools import lru_cache
from http import HTTPStatus
from typing import Optional

import aiohttp
from aiohttp import ClientResponse
from aiohttp import ContentTypeError
from starlette import status


@lru_cache
class BaseRequestsClient:
    base_url: str = NotImplemented
    auth: dict = NotImplemented
    raise_exceptions: bool = NotImplemented

    def get_error_message(self, status_code: int, msg: Optional[str] = None) -> str:
        return (
            f"{self.base_url} responded with bad status code of {status_code}. "
            f"Additional message: {msg}. "
            f"Actual API response in the details"
        )

    @staticmethod
    def handle_error(error_msg: str, response: str, raise_exceptions: bool) -> None:
        logging.error(str(dict(error_msg=error_msg, response=response)))
        if raise_exceptions:
            raise RuntimeError(f"Error while accessing external service: {response}")

    async def _parse_answer(
        self,
        resp: ClientResponse,
        url: str,
        data: dict,
        headers: dict,
        params: dict,
        json: dict,
        raise_exceptions: bool,
        return_json: bool,
    ) -> ClientResponse | dict:
        if resp.status == HTTPStatus.NO_CONTENT:
            return resp

        text = await resp.text(encoding="utf-8")

        if resp.status in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
            msg = (
                f"Unauthorized. Request response: {text=}  "  # noqa
                f"Requested: {url=} {params=} {data=} {json=} {headers=}"
            )
            self.handle_error(error_msg=msg, response=text, raise_exceptions=raise_exceptions)

        elif resp.status >= status.HTTP_400_BAD_REQUEST:
            msg = f"Got {resp.status=}, resp={text} Requested: {url=} {params=} {data=} {json=} {headers=}"  # noqa
            self.handle_error(error_msg=msg, response=text, raise_exceptions=raise_exceptions)

        logging.info(f"When accessing to {url}, Got {text=}")

        if return_json:
            try:
                return await resp.json(encoding="utf-8")
            except ContentTypeError as e:
                logging.error(
                    f"Cannot parse json. resp={text}, {resp.status=} ",
                    f"{url=} {params=} {data=} {json=} {headers=}",
                )
                raise e

        return resp

    async def _make_request(
        self,
        method: str,
        url: str,
        data: dict | str | list = None,
        json: dict | str | list = None,
        params: dict | str | list = None,
        headers: Optional[dict] = None,
        return_json: Optional[bool] = True,
        raise_exceptions: Optional[bool] = None,
    ) -> ClientResponse | dict:
        url = self.base_url + url
        final_headers = self.auth.copy()
        timeout = aiohttp.ClientTimeout(total=60)

        if raise_exceptions is None:
            raise_exceptions = self.raise_exceptions

        if headers:
            final_headers |= headers

        if return_json is True:
            final_headers |= {
                "accept": "application/json",
                "Content-Type": "application/json",
            }

        kwargs = dict(method=method, url=url, data=data, timeout=timeout, json=json, params=params)

        logging.info(f"Sending {method} request to {url=} " f"{data=} {headers=} {params=} {json=}")

        async with aiohttp.ClientSession(headers=final_headers) as session:
            async with session.request(**kwargs) as resp:
                return await self._parse_answer(
                    resp=resp,
                    url=url,
                    data=data,
                    headers=final_headers,
                    params=params,
                    json=json,
                    raise_exceptions=raise_exceptions,
                    return_json=return_json,
                )
