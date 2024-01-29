import asyncio
import dataclasses

import aiohttp


@dataclasses.dataclass
class PathfinderArchiveOfNethysDocument:
    """
    Represents an essential document for Archive of Nethys.
    """

    id: str
    name: str
    text: str
    url: str


class PathfinderArchiveOfNethysClient:
    """
    Simple PathfinderWikiClient
    """

    def __init__(self):
        self.session = None
        self._aon_elasticsearch_base_url = (
            "https://elasticsearch.aonprd.com/aon/_search"
        )
        self._max_size = 10

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def search_pages(self, query: str) -> list[PathfinderArchiveOfNethysDocument]:
        """
            Searches the Archive of Nethys pages
        :param query: The search query.
        :return: A list of: func:`PathfinderWikiPage`.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

        found_items = []
        async with self.session.post(
            self._aon_elasticsearch_base_url,
            json={
                "query": {
                    "query_string": {"query": f"{query}*", "default_field": "name"}
                },
                "fields": ["name", "text", "url"],
                "_source": False,
            },
        ) as response:
            result = await response.json()
            for item in result.get("hits", {}).get("hits", []):
                found_items.append(
                    PathfinderArchiveOfNethysDocument(
                        id=item.get("_id"),
                        name=item.get("fields", {}).get("name", ["Unknown"])[0],
                        text=item.get("fields", {}).get("text", ["Unknown"])[0],
                        url=item.get("fields", {}).get("url", ["Unknown"])[0],
                    )
                )
            return found_items

    @staticmethod
    def get_page_link(page_url) -> str:
        return f"https://2e.aonprd.com/{page_url}"

    async def close(self):
        await self.session.close()


if __name__ == "__main__":
    pf = PathfinderArchiveOfNethysClient()
    result = asyncio.run(pf.search_pages("zom"))
    print(result)
    for item in result:
        print(pf.get_page_link(item.url))

    asyncio.run(pf.close())
