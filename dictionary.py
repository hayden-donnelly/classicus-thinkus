import discord
from discord.ext import commands
import urllib.request
import json
import main

class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='define_test')
    async def define_test(self, ctx, word):
        with urllib.request.urlopen("https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
                                        + word + "?key=" + main.mw_collegiate_key) as f:
            data = json.loads(f.read().decode())
            embed = discord.Embed(title=word, description=data[0]['shortdef'][0])
            embed.set_footer(text="Merriam-Webster Collegiate Dictionary")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Dictionary(bot))