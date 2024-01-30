import asyncio
import dataclasses
import typing

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

    async def search_page_by_id(
        self, document_id: str
    ) -> typing.Optional[PathfinderArchiveOfNethysDocument]:
        """
            Searches the Archive of Nethys by an id.
        :param document_id: - The document id.
        :return: - The Archive of Nethys document.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

        if document_id == "":
            return None

        async with self.session.post(
            self._aon_elasticsearch_base_url,
            json={
                "size": 1,
                "query": {
                    "query_string": {
                        "query": f"{document_id}",
                        "default_field": "id",
                    }
                },
                "fields": ["name", "text", "url"],
                "_source": False,
            },
        ) as response:
            result = await response.json()
            for item in result.get("hits", {}).get("hits", []):
                return PathfinderArchiveOfNethysDocument(
                    id=item.get("_id"),
                    name=item.get("fields", {}).get("name", ["Unknown"])[0],
                    text=item.get("fields", {}).get("text", ["Unknown"])[0],
                    url=item.get("fields", {}).get("url", ["Unknown"])[0],
                )

    async def search_pages(
        self, query: str, size: int = 10
    ) -> list[PathfinderArchiveOfNethysDocument]:
        """
            Searches the Archive of Nethys pages
        :param query: The search query.
        :param size: The maximum number of items to return in a single query.
        :return: A list of: func:`PathfinderWikiPage`.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

        if query == "":
            return []

        found_items = []
        async with self.session.post(
            self._aon_elasticsearch_base_url,
            json={
                "size": size,
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
    def format_url(page_url) -> str:
        """
        Formats an archive of nethys url into a full url.
        """
        return f"https://2e.aonprd.com/{page_url}"

    async def close(self):
        await self.session.close()


if __name__ == "__main__":
    pf = PathfinderArchiveOfNethysClient()
    result = asyncio.run(pf.search_pages("zom"))
    print(result)
    for item in result:
        print(pf.format_url(item.url))

    asyncio.run(pf.close())
