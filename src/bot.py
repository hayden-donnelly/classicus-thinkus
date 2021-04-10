import global_vars as gv

#@gv.bot.event
#async def on_ready():
#    print("Everything's all ready to go~")

#@gv.bot.event
#async def on_message(message):
#    print("The message's content was", message.content)
#    await bot.process_commands(message)

if __name__ == '__main__':
    gv.init()
    command_extensions =    ['cogs.dictionary', 
                            'cogs.embeds', 
                            'cogs.settings', 
                            'cogs.suggestions',
                            'cogs.backend']

    for extension in command_extensions:
        try:
            gv.bot.load_extension(extension)
        except (AttributeError, ImportError) as e:
            print("Error\n")

    gv.bot.run(gv.discord_key)