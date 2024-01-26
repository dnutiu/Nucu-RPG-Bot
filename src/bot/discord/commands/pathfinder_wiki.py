import disnake
from disnake.ext import commands

from src.knowledge.pathfinder_wiki import PathfinderWikiClient


async def pathfinder_wiki_lookup_autocomplete(
    inter: disnake.ApplicationCommandInteraction, user_input: str
) -> list[str]:
    async with PathfinderWikiClient() as wiki_client:
        data = await wiki_client.search_pages(user_input)
        return list(map(lambda x: x.key, data))


class PathfinderWikiCog(commands.Cog):
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
        wiki_link = PathfinderWikiClient.get_wiki_page_url(query)
        await inter.send(f"@{inter.author} here's the wiki link: {wiki_link}")
