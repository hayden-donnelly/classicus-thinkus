import discord
from discord.ext import commands

class Alternate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testing(self, ctx):
        await ctx.send("Testing")