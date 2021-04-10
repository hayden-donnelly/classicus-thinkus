import discord
from discord.ext import commands
import pandas as pd
import os
import time

def init():
    global prefix, bot, help_text_file, help_text, keys, discord_key, mw_collegiate_key, mw_medical_key, settings, start_time
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