"""
    Pathfinder Wiki commands.
"""
import disnake
from disnake.ext import commands

from src.knowledge.pathfinder.wiki import PathfinderWikiClient


async def pathfinder_wiki_lookup_autocomplete(
    inter: disnake.ApplicationCommandInteraction, user_input: str
) -> list[str]:
    """
    Autocompletes pathfinder wiki queries.
    """
    async with PathfinderWikiClient() as wiki_client:
        data = await wiki_client.search_pages(user_input)
        return list(map(lambda x: x.key, data))


class PathfinderWikiCog(commands.Cog):
    """
    PathfinderWikiCog implements commands related to the pathfinder wiki.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="pf-wiki-lookup", description="Lookup a Pathfinder wiki page."
    )
    async def lookup(
        self,
        inter: disnake.ApplicationCommandInteraction,
        query: str = commands.Param(autocomplete=pathfinder_wiki_lookup_autocomplete),
    ):
        """
        Looks up a page on Pathfinder wiki.
        """
        wiki_link = PathfinderWikiClient.get_page_link(query)
        await inter.send(f"@{inter.author} here's the wiki link: {wiki_link}")
