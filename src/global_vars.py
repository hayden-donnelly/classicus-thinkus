import discord
from discord.ext import commands
import pandas as pd
import os
import time

def init():
    global prefix, bot, hidden_file_path, help_text_file, help_text, keys, discord_key, mw_collegiate_key, mw_medical_key, settings, start_time
    prefix = "?"
    bot = commands.Bot(command_prefix=prefix)
    hidden_file_path = '../../'
    help_text_file = open(os.path.abspath('data/help.txt'))
    help_text = help_text_file.read()

    keys = pd.read_csv(os.path.abspath(hidden_file_path + 'api_keys.csv'))
    discord_key = str(keys[keys['API'] == 'Discord']['Key'].values[0])
    mw_collegiate_key = str(keys[keys['API'] == 'MW Collegiate']['Key'].values[0])
    mw_medical_key = str(keys[keys['API'] == 'MW Medical']['Key'].values[0])

    settings = pd.read_csv(os.path.abspath(hidden_file_path + 'settings.csv'))
    settings = settings.set_index('Guild ID')

    start_time = time.time()