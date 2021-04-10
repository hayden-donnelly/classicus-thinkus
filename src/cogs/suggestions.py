import discord
from discord.ext import commands
import json
import global_vars as gv
import utility as ut

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, suggestion):
        channel = gv.bot.get_channel(gv.settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'])
        embed = discord.Embed(title="New Suggestion", description=suggestion, 
                                color=ut.readable_hex(gv.settings.loc[ctx.message.guild.id, 'Suggestion New Color']))
        embed.set_author(name=ctx.author.name + " | " + str(ctx.author.id), icon_url=ctx.author.avatar_url)
        message = await channel.send(embed=embed)
        await message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        await message.add_reaction("\N{CROSS MARK}")

    @commands.command()
    async def suggestion_accept(self, ctx, suggestion_id, reason):
        channel = gv.bot.get_channel(gv.settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'])
        message = await channel.fetch_message(suggestion_id)
        old_embed = message.embeds[0]
        new_embed = discord.Embed(title="Accepted Suggestion", description=old_embed.description, 
                                    color=ut.readable_hex(gv.settings.loc[ctx.message.guild.id, 'Suggestion Accepted Color']))
        new_embed.set_author(name=old_embed.author.name, icon_url=old_embed.author.icon_url)
        new_embed.add_field(name=ctx.author.name + "'s Reason", value=reason, inline=False)
        await message.edit(embed=new_embed)
        await ctx.send("Suggestion " + str(suggestion_id) + " has been accepted.")

    @commands.command()
    async def suggestion_deny(self, ctx, suggestion_id, reason):
        channel = gv.bot.get_channel(gv.settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'])
        message = await channel.fetch_message(suggestion_id)
        old_embed = message.embeds[0]
        new_embed = discord.Embed(title="Denied Suggestion", description=old_embed.description, 
                                    color=ut.readable_hex(gv.settings.loc[ctx.message.guild.id, 'Suggestion Denied Color']))
        new_embed.set_author(name=old_embed.author.name, icon_url=old_embed.author.icon_url)
        new_embed.add_field(name=ctx.author.name + "'s Reason", value=reason, inline=False)
        await message.edit(embed=new_embed)
        await ctx.send("Suggestion " + str(suggestion_id) + " has been denied.")

    @commands.command()
    async def suggestion_maybe(self, ctx, suggestion_id, reason):
        channel = gv.bot.get_channel(gv.settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'])
        message = await channel.fetch_message(suggestion_id)
        old_embed = message.embeds[0]
        new_embed = discord.Embed(title="Potential Suggestion", description=old_embed.description, 
                                    color=ut.readable_hex(gv.settings.loc[ctx.message.guild.id, 'Suggestion Potential Color']))
        new_embed.set_author(name=old_embed.author.name, icon_url=old_embed.author.icon_url)
        new_embed.add_field(name=ctx.author.name + "'s Reason", value=reason, inline=False)
        await message.edit(embed=new_embed)
        await ctx.send("Suggestion " + str(suggestion_id) + " is under review.")

    @commands.command()
    @commands.has_role("Admin")
    async def suggestion_channel(self, ctx, channel_id):
        channel_id = ut.cleanup_channel_id(channel_id)
        gv.settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'] = channel_id
        await ctx.send("Suggestion channel has been set to: " + str(channel_id))

    @commands.command()
    @commands.has_role("Admin")
    async def suggestion_new_color(self, ctx, color):
        gv.settings.loc[ctx.message.guild.id, 'Suggestion New Color'] = str(color)
        await ctx.send("Suggestion new color has been set to: " + color)

    @commands.command()
    @commands.has_role("Admin")
    async def suggestion_accepted_color(self, ctx, color):
        gv.settings.loc[ctx.message.guild.id, 'Suggestion Accepted Color'] = str(color)
        await ctx.send("Suggestion accepted color has been set to: " + color)

    @commands.command()
    @commands.has_role("Admin")
    async def suggestion_denied_color(self, ctx, color):
        gv.settings.loc[ctx.message.guild.id, 'Suggestion Denied Color'] = str(color)
        await ctx.send("Suggestion denied color has been set to: " + color)

    @commands.command()
    @commands.has_role("Admin")
    async def suggestion_potential_color(self, ctx, color):
        gv.settings.loc[ctx.message.guild.id, 'Suggestion Potential Color'] = str(color)
        await ctx.send("Suggestion potential color has been set to: " + color)

def setup(bot):
    bot.add_cog(Suggestions(bot))