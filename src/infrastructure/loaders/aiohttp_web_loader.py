import aiohttp

from src.application.interfaces import WebPageLoader

type url = str


class AiohttpWebLoader(WebPageLoader):
    async def load(self, page_url: url) -> str:
        """
        Loads the content of a web page.

        :param page_url: URL of the web page.
        :return: Content of the web page.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(page_url) as response:
                response.raise_for_status()
                return await response.text()
