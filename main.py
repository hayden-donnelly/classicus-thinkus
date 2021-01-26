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

    #if client.user.mention in message.content.split(" "):
    if client.user.mentioned_in(message):
        await message.channel.send("Nyeah eh? Waste yute tryna mess with me eh?? Mans bout to catch this defaz real quick")
    if message.content.startswith(command_prefix + 'say'):
        await message.delete()
        await message.channel.send(message.content.split("/say",1)[1])

token = input()
client.run(token)