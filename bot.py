import global_vars as gv

if __name__ == '__main__':
    gv.init()
    initial_extensions = ['cogs.dictionary', 'cogs.embeds', 'cogs.settings']

    for extension in initial_extensions:
        try:
            gv.bot.load_extension(extension)
        except (AttributeError, ImportError) as e:
            print("Error\n")

    gv.bot.run(gv.discord_key)