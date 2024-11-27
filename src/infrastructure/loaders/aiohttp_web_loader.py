import aiohttp

from src.interface_adapters.exceptions import PageLoadingError
from src.application.interfaces import WebPageLoader

type url = str


class AiohttpWebLoader(WebPageLoader):
    async def load(self, page_url: url) -> str:
        """
        Loads the content of a web page.

        :param page_url: URL of the web page.
        :return: Content of the web page.
        """
        async with aiohttp.ClientSession(trust_env=True) as session:
            try:
                async with session.get(page_url) as response:
                    try:
                        response.raise_for_status()
                    except aiohttp.ClientResponseError as e:
                        raise PageLoadingError from e
                    content: str = await response.text()
                    return content
            except aiohttp.ClientError as e:
                raise PageLoadingError from e
