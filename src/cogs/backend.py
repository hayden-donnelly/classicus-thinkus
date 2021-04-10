import discord
from discord.ext import commands
import time
import global_vars as gv

class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Admin")
    async def h(self, ctx):
        title = "Commands"
        embed = discord.Embed(title=title, description=gv.help_text)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role("Admin")
    async def uptime(self, ctx):
        await ctx.send("Uptime: " + str(int(time.time() - gv.start_time)) + " seconds.")

def setup(bot):
    bot.add_cog(Dictionary(bot))