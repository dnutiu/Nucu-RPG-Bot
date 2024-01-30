import datetime

import disnake
import re
from disnake.ext import commands

from src.knowledge.pathfinder_archive_of_nethys import PathfinderArchiveOfNethysClient


async def pathfinder_aon_lookup_autocomplete(
    inter: disnake.ApplicationCommandInteraction, user_input: str
) -> list[str]:
    """
    Autocompletes pathfinder archive of nethys queries.
    """
    async with PathfinderArchiveOfNethysClient() as aon_client:
        if user_input == "":
            return [
                "(archetype-182) Zombie",
                "(archetype-26) Recall Knowledge",
                "(rules-458) Flanking",
                "(rules-733) Runes",
                "(rules-1115) Diseases",
                "(class-23) Kineticist",
                "(rules-1133) Magic",
                "(rules-28) Golarion",
                "(rules-387) Actions",
                "(rules-1026) Action Economy",
            ]
        data = await aon_client.search_pages(user_input)
        return list(map(lambda x: f"({x.id}) - {x.name}", data))


class PathfinderArchiveOfNethysButton(disnake.ui.View):
    """
    PathfinderArchiveOfNethysButton adds a view button for visiting an archive of nethys link.
    """

    def __init__(self, url: str):
        super().__init__()
        self.add_item(disnake.ui.Button(label="View Page", url=url))


class PathfinderArchiveOfNethysCog(commands.Cog):
    """
    PathfinderArchiveOfNethysCog is the Cog that implements Pathfinder Archive of Nethys related commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self._id_regex = r"\((.*)\) .*"

    @commands.slash_command(name="aon", description="Lookup a Archive of Nethys page.")
    async def lookup(
        self,
        inter: disnake.ApplicationCommandInteraction,
        query: str = commands.Param(autocomplete=pathfinder_aon_lookup_autocomplete),
    ):
        """
        Looks up a page on Archive of Nethys.
        """
        async with PathfinderArchiveOfNethysClient() as aon_client:
            match = re.match(self._id_regex, query)
            if match:
                data = await aon_client.search_page_by_id(document_id=match.groups()[0])
            else:
                data = await aon_client.search_pages(query)
                if len(data) == 0:
                    data = None
                else:
                    data = data[0]
            if data is None:
                await inter.send(
                    f"@{inter.author} nothing was found for the given query: {query}"
                )
            else:
                embed = disnake.Embed(
                    title=data.name,
                    description=data.text,
                    timestamp=datetime.datetime.now(),
                )
                await inter.send(
                    f"@{inter.author} requested {query}",
                    embed=embed,
                    view=PathfinderArchiveOfNethysButton(
                        url=aon_client.format_url(data.url)
                    ),
                )
