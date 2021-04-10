import discord
from discord.ext import commands
import pandas as pd
import os

from alternate import Alternate

prefix = "?"
bot = commands.Bot(command_prefix=prefix)
keys = pd.read_csv(os.path.abspath("../../api_keys.csv"))
discord_key = str(keys[keys['API'] == 'Discord']['Key'].values[0])


bot.add_cog(Alternate(bot))

bot.run(discord_key)