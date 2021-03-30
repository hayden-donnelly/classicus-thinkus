import discord
import json
import urllib.request
import pandas as pd
import os
from discord.ext import commands

# Backend utility
def readable_hex(color):
    return(int(hex(int(color, 16)), 0))

def cleanup_channel_id(channel_id):
    channel_id = channel_id.replace('<', '')
    channel_id = channel_id.replace('>', '')
    channel_id = channel_id.replace('#', '')
    channel_id = int(channel_id)
    return channel_id    

def save_settings(settings):
    settings.to_csv(os.path.abspath("../../settings.csv"), index=False)

#column_names = ["Guild ID", "Embed Channel ID", "Embed Default Color", "Suggestion Channel ID", "Suggestion New Color", "Suggestion Accepted Color", "Suggestion Denied Color", "Suggestion Potential Color"]
#df = pd.DataFrame(columns=column_names)

# Settings
prefix = "?"
bot = commands.Bot(command_prefix=prefix)
help_text_file = open("help.txt")
help_text = help_text_file.read()
suggestion_channel_id = ""
suggestion_color_hex = readable_hex("f3785d")
embed_channel_id = 0
embed_default_color_hex = readable_hex("000000")

keys = pd.read_csv(os.path.abspath("../../api_keys.csv"))
discord_key = str(keys[keys['API'] == 'Discord']['Key'].values[0])
mw_collegiate_key = str(keys[keys['API'] == 'MW Collegiate']['Key'].values[0])
mw_medical_key = str(keys[keys['API'] == 'MW Medical']['Key'].values[0])

settings = pd.read_csv(os.path.abspath("../../settings.csv", index=False))
#df.read_csv(filename, index=False) 

#new_row = {'name':'Geo', 'physics':87, 'chemistry':92, 'algebra':97}
#df_marks = df_marks.append(new_row, ignore_index=True)
#df.loc[20]['Embed Channel ID'] = 20

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
async def init_guild(ctx):
    global settings
    settings = settings.append({'Guild ID':ctx.message.guild.id, 'Embed Channel ID':-1, 
                                'Embed Default Color':readable_hex("000000"), 'Suggestion Channel ID':-1,
                                'Suggestion New Color':readable_hex("000000"), 'Suggestion Accepted Color':readable_hex("000000"),
                                'Suggestion Denied Color':readable_hex("000000"), 'Suggestion Potential Color':readable_hex("000000")}, 
                                ignore_index=True)
    settings = settings.set_index('Guild ID')
    save_settings(settings)

# Embeds
@bot.command(pass_context=True)
@commands.has_role("Admin")
async def embed_simple(ctx, title, body, color, image):
    channel = bot.get_channel(embed_channel_id)
    color = embed_default_color_hex if color == "" else readable_hex(color)
    embed = discord.Embed(title=title, description=body, color=color)
    embed.set_image(url=image)
    await channel.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def embed_json(ctx):
    await ctx.send("This command has not been setup yet.")

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def embed_channel(ctx, channel_id):
    channel_id = cleanup_channel_id(channel_id)
    global embed_channel_id
    embed_channel_id = channel_id
    await ctx.send("Embed channel has been set to: " + str(channel_id))

# Suggestions
@bot.command(pass_context=True)
async def suggest(ctx, suggestion):
    channel = bot.get_channel(suggestion_channel_id)
    embed = discord.Embed(title="New Suggestion", description=suggestion, color=suggestion_color_hex)
    #embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_author(name=ctx.author.name + " | " + str(ctx.author.id), icon_url=ctx.author.avatar_url)
    message = await channel.send(embed=embed)
    await message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
    await message.add_reaction("\N{CROSS MARK}")

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def suggestion_channel(ctx, channel_id):
    channel_id = cleanup_channel_id(channel_id)
    global suggestion_channel_id
    suggestion_channel_id = channel_id
    await ctx.send("Suggestion channel has been set to: " + str(channel_id))

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def suggestion_color(ctx, color):
    global suggestion_color_hex 
    suggestion_color_hex = readable_hex(color)
    await ctx.send("Suggestion color has been set to: " + color)

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