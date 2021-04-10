import discord
from discord.ext import commands
import os
import global_vars as gv

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Admin")
    async def settings_init(self, ctx):
        guild_id = ctx.message.guild.id
        if guild_id in gv.settings.index:
            await ctx.send("Settings have already been initialized for this guild.")
        else:
            gv.settings = gv.settings.append({'Guild ID':guild_id, 'Embed Channel ID':-1, 
                                        'Embed Default Color':"000000", 'Suggestion Channel ID':-1,
                                        'Suggestion New Color':"000000", 'Suggestion Accepted Color':"000000",
                                        'Suggestion Denied Color':"000000", 'Suggestion Potential Color':"000000"}, 
                                        ignore_index=True)
            gv.settings = gv.settings.set_index('Guild ID')
            await ctx.send("Settings have been initialized.")

    @commands.command()
    @commands.has_role("Admin")
    async def settings_save(self, ctx):
        gv.settings.to_csv(os.path.abspath("../../settings.csv"))
        await ctx.send("Settings have been saved.")

    @commands.command()
    @commands.has_role("Admin")
    async def settings_display(self, ctx):
        embed = discord.Embed(title='Guild Settings', description=str(gv.settings.loc[ctx.message.guild.id]))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Settings(bot))