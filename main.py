import discord
import os

client = discord.Client()
command_prefix = '/'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_prefix + 'say'):
        await message.delete();
        await message.channel.send(message.content.split("/say",1)[1])

token = input()
client.run(token)