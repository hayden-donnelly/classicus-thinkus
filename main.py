import discord
import json
import urllib.request
import pandas as pd
import os
from discord.ext import commands
import time

# Backend utility
def readable_hex(color):
    return(int(hex(int(color, 16)), 0))

def cleanup_channel_id(channel_id):
    channel_id = channel_id.replace('<', '')
    channel_id = channel_id.replace('>', '')
    channel_id = channel_id.replace('#', '')
    channel_id = int(channel_id)
    return channel_id    

#column_names = ["Guild ID", "Embed Channel ID", "Embed Default Color", "Suggestion Channel ID", "Suggestion New Color", "Suggestion Accepted Color", "Suggestion Denied Color", "Suggestion Potential Color"]
#data = {"Guild ID":20, "Embed Channel ID":20, "Embed Default Color":20, "Suggestion Channel ID":20, "Suggestion New Color":20, "Suggestion Accepted Color":20, "Suggestion Denied Color":20, "Suggestion Potential Color":20}
#df = pd.DataFrame(columns=column_names)

# Settings
prefix = "?"
bot = commands.Bot(command_prefix=prefix)
help_text_file = open("help.txt")
help_text = help_text_file.read()

keys = pd.read_csv(os.path.abspath("../../api_keys.csv"))
discord_key = str(keys[keys['API'] == 'Discord']['Key'].values[0])
mw_collegiate_key = str(keys[keys['API'] == 'MW Collegiate']['Key'].values[0])
mw_medical_key = str(keys[keys['API'] == 'MW Medical']['Key'].values[0])

settings = pd.read_csv(os.path.abspath("../../settings.csv"))
settings = settings.set_index('Guild ID')

start_time = time.time()

@bot.event
async def on_ready():
    print("Everything's all ready to go~")

@bot.event
async def on_message(message):
    print("The message's content was", message.content)
    await bot.process_commands(message)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def h(ctx):
    title = "Commands"
    embed = discord.Embed(title=title, description=help_text)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def uptime(ctx):
    await ctx.send("Uptime: " + str(int(time.time() - start_time)) + " seconds.")

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def settings_init(ctx):
    global settings
    guild_id = ctx.message.guild.id
    if guild_id in settings.index:
        await ctx.send("Settings have already been initialized for this guild.")
    else:
        settings = settings.append({'Guild ID':guild_id, 'Embed Channel ID':-1, 
                                    'Embed Default Color':"000000", 'Suggestion Channel ID':-1,
                                    'Suggestion New Color':"000000", 'Suggestion Accepted Color':"000000",
                                    'Suggestion Denied Color':"000000", 'Suggestion Potential Color':"000000"}, 
                                    ignore_index=True)
        settings = settings.set_index('Guild ID')
        await ctx.send("Settings have been initialized.")

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def settings_save(ctx):
    global settings
    settings.to_csv(os.path.abspath("../../settings.csv"))
    await ctx.send("Settings have been saved.")

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def settings_display(ctx):
    global settings
    embed = discord.Embed(title='Guild Settings', description=str(settings.loc[ctx.message.guild.id]))
    await ctx.send(embed=embed)

# Embeds
@bot.command(pass_context=True)
@commands.has_role("Admin")
async def embed_simple(ctx, title, body, color, image):
    global settings
    channel = bot.get_channel(settings.loc[ctx.message.guild.id, 'Embed Channel ID'])
    color = readable_hex(settings.loc[ctx.message.guild.id, 'Embed Default Color']) if color == "" else readable_hex(color)
    embed = discord.Embed(title=title, description=body, color=color)
    embed.set_image(url=image)
    await channel.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def embed_json(ctx):
    await ctx.send("This command has not been setup yet.")

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def embed_simple_edit(ctx, embed_id, title, body, color, image):
    global settings
    channel = bot.get_channel(settings.loc[ctx.message.guild.id, 'Embed Channel ID'])
    color = readable_hex(settings.loc[ctx.message.guild.id, 'Embed Default Color']) if color == "" else readable_hex(color)
    embed = discord.Embed(title=title, description=body, color=color)
    embed.set_image(url=image)
    original_embed = await channel.fetch_message(embed_id)
    await original_embed.edit(embed=embed)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def embed_json_edit(ctx):
    await ctx.send("This command has not been setup yet.")

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def embed_channel(ctx, channel_id):
    channel_id = cleanup_channel_id(channel_id)
    global settings
    settings.loc[ctx.message.guild.id, 'Embed Channel ID'] = channel_id
    await ctx.send("Embed channel has been set to: " + str(channel_id))

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def embed_default_color(ctx, color):
    global settings
    settings.loc[ctx.message.guild.id, 'Embed Default Color'] = str(color)
    await ctx.send("Embed default color has been set to: " + color)

# Suggestions
@bot.command(pass_context=True)
async def suggest(ctx, suggestion):
    global settings
    channel = bot.get_channel(settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'])
    embed = discord.Embed(title="New Suggestion", description=suggestion, 
                            color=readable_hex(settings.loc[ctx.message.guild.id, 'Suggestion New Color']))
    embed.set_author(name=ctx.author.name + " | " + str(ctx.author.id), icon_url=ctx.author.avatar_url)
    message = await channel.send(embed=embed)
    await message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
    await message.add_reaction("\N{CROSS MARK}")

@bot.command(pass_context=True)
async def suggestion_accept(ctx, suggestion_id, reason):
    global settings
    channel = bot.get_channel(settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'])
    message = await channel.fetch_message(suggestion_id)
    old_embed = message.embeds[0]
    new_embed = discord.Embed(title="Accepted Suggestion", description=old_embed.description, 
                                color=readable_hex(settings.loc[ctx.message.guild.id, 'Suggestion Accepted Color']))
    new_embed.set_author(name=old_embed.author.name, icon_url=old_embed.author.icon_url)
    new_embed.add_field(name=ctx.author.name + "'s Reason", value=reason, inline=False)
    await message.edit(embed=new_embed)
    await ctx.send("Suggestion " + str(suggestion_id) + " has been accepted.")

@bot.command(pass_context=True)
async def suggestion_deny(ctx, suggestion_id, reason):
    global settings
    channel = bot.get_channel(settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'])
    message = await channel.fetch_message(suggestion_id)
    old_embed = message.embeds[0]
    new_embed = discord.Embed(title="Denied Suggestion", description=old_embed.description, 
                                color=readable_hex(settings.loc[ctx.message.guild.id, 'Suggestion Denied Color']))
    new_embed.set_author(name=old_embed.author.name, icon_url=old_embed.author.icon_url)
    new_embed.add_field(name=ctx.author.name + "'s Reason", value=reason, inline=False)
    await message.edit(embed=new_embed)
    await ctx.send("Suggestion " + str(suggestion_id) + " has been denied.")

@bot.command(pass_context=True)
async def suggestion_maybe(ctx, suggestion_id, reason):
    global settings
    channel = bot.get_channel(settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'])
    message = await channel.fetch_message(suggestion_id)
    old_embed = message.embeds[0]
    new_embed = discord.Embed(title="Potential Suggestion", description=old_embed.description, 
                                color=readable_hex(settings.loc[ctx.message.guild.id, 'Suggestion Potential Color']))
    new_embed.set_author(name=old_embed.author.name, icon_url=old_embed.author.icon_url)
    new_embed.add_field(name=ctx.author.name + "'s Reason", value=reason, inline=False)
    await message.edit(embed=new_embed)
    await ctx.send("Suggestion " + str(suggestion_id) + " is under review.")

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def suggestion_channel(ctx, channel_id):
    channel_id = cleanup_channel_id(channel_id)
    global settings
    settings.loc[ctx.message.guild.id, 'Suggestion Channel ID'] = channel_id
    await ctx.send("Suggestion channel has been set to: " + str(channel_id))

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def suggestion_new_color(ctx, color):
    global settings
    settings.loc[ctx.message.guild.id, 'Suggestion New Color'] = str(color)
    await ctx.send("Suggestion new color has been set to: " + color)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def suggestion_accepted_color(ctx, color):
    global settings
    settings.loc[ctx.message.guild.id, 'Suggestion Accepted Color'] = str(color)
    await ctx.send("Suggestion accepted color has been set to: " + color)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def suggestion_denied_color(ctx, color):
    global settings
    settings.loc[ctx.message.guild.id, 'Suggestion Denied Color'] = str(color)
    await ctx.send("Suggestion denied color has been set to: " + color)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def suggestion_potential_color(ctx, color):
    global settings
    settings.loc[ctx.message.guild.id, 'Suggestion Potential Color'] = str(color)
    await ctx.send("Suggestion potential color has been set to: " + color)

# Dictionary
@bot.command(pass_context=True)
async def define(ctx, word):
    with urllib.request.urlopen("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" 
                                + word + "?key=" + mw_collegiate_key) as f:
        data = json.loads(f.read().decode())
        embed = discord.Embed(title=word, description=data[0]['shortdef'][0])
        embed.set_footer(text="Merriam-Webster Collegiate Dictionary")
        await ctx.send(embed=embed)

# Connect to Discord
bot.run(discord_key)