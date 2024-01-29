import asyncio
import dataclasses

import aiohttp
from pydantic_core import Url


@dataclasses.dataclass
class PathfinderWikiPage:
    key: str
    title: str
    excerpt: str
    image: Url


class PathfinderWikiClient:
    """
    Simple PathfinderWikiClient
    """

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def search_pages(self, query: str) -> list[PathfinderWikiPage]:
        """
            Searches the wiki pages that match the given query.
        :param query: The wiki query.
        :return: A list of: func:`PathfinderWikiPage`.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

        def _convert_to_page(item) -> PathfinderWikiPage:
            image = None
            thumbnail = item.get("thumbnail", {})
            if thumbnail is not None:
                image = thumbnail.get("image")
            return PathfinderWikiPage(
                key=item.get("key"),
                title=item.get("title"),
                excerpt=item.get("excerpt"),
                image=image,
            )

        async with self.session.get(
            f"https://pathfinderwiki.com/w/rest/v1/search/title?q={query}&limit=10"
        ) as response:
            result = await response.json()
            return list(map(_convert_to_page, result.get("pages", [])))

    @staticmethod
    def get_page_link(page_key) -> str:
        return f"https://pathfinderwiki.com/wiki/{page_key}"

    async def close(self):
        await self.session.close()


if __name__ == "__main__":
    pf = PathfinderWikiClient()
    asyncio.run(pf.search_pages("zom"))
    print(pf.get_page_link("zombie_lord"))

    asyncio.run(pf.close())
