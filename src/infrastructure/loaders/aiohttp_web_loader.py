from src.application.interfaces import WebPageLoader

type url = str


class AiohttpWebLoader(WebPageLoader):
    async def load(self, page_url: url) -> str:
        """
        Loads the content of a web page.

        :param page_url: URL of the web page.
        :return: Content of the web page.
        """
        raise NotImplementedError  # TODO: Implement loading the content of a web page using aiohttp.
