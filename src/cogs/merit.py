import discord
from discord.ext import commands
import pandas as pd
import plotly.express as px
from datetime import date
import global_vars as gv
import re

class Merit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.merit_log = pd.read_csv(gv.hidden_file_path + 'test_data.csv', index_col='Date', parse_dates=True)
        except:
            self.merit_log = pd.DataFrame()
        try:
            self.message_data = pd.read_csv(gv.hidden_file_path + 'message_data.csv')
        except:
            self.message_data = pd.DataFrame()

    def new_merit_log_entry(self, ctx, user_id, merit, demerit):
        entry = {'Guild ID': ctx.message.guild.id, 'User ID': user_id, 
                'Merit': merit, 'Demerit': demerit, 'Date': str(date.today())}
        # Todo: maybe change ignore_index so it doesn't delete the date time index
        self.merit_log = self.merit_log.append(entry, ignore_index=True)
        self.merit_log.to_csv(gv.hidden_file_path + 'test_data.csv')

    @commands.command()
    @commands.has_role("Admin")
    async def merit(self, ctx, user_id):
        self.new_merit_log_entry(ctx, user_id, 1, 0)
        await ctx.send("Merit point has been granted.")

    @commands.command()
    @commands.has_role("Admin")
    async def demerit(self, ctx, user_id):
        self.new_merit_log_entry(ctx, user_id, 0, 1)
        await ctx.send("Demerit point has been granted.")

    @commands.command()
    @commands.has_role("Admin")
    async def merit_history(self, ctx, user_id):
        data = self.merit_log[(self.merit_log['Guild ID'] == ctx.message.guild.id) & (self.merit_log['User ID'] == user_id)]
        data = data.drop(columns=['Guild ID', 'User ID'])
        data = data.resample('D').sum()
        data = data.reset_index()

        fig = px.line(x='Date', y=['Merit', 'Demerit'], data_frame=data, title='Merit/Demerit History')
        fig.write_image(gv.hidden_file_path + 'merit_history.png')
        await ctx.send(file=discord.File(gv.hidden_file_path + 'merit_history.png'))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            ctx = await self.bot.get_context(message)

            message_string = re.sub(r'\:.*\:', '', message.content) # Remove emotes from message
            message_string = re.sub(r'http\S+', '', message_string) # Remove links from message

            word_count = len(message_string.split(' '))
            character_count = len(message_string.replace(' ', ''))
            mean_character_count = word_count / character_count

            # Todo: maybe keep 'date.today' as its original data type instead of converting to string.
            # This might make it easier to convert the column into a date time index.
            entry = {'Date': str(date.today), 'Guild ID': ctx.message.guild.id, 'User ID': ctx.message.author.id, 
                        'Word Count': word_count, 'Character Count': character_count, 'Mean Character Count': mean_character_count,
                        'Message Link': message.jump_url}
            self.message_data = self.message_data.append(entry, ignore_index=True)

            # Todo: maybe set this to be a periodic process instead of running everytime a message is sent
            self.message_data.to_csv(gv.hidden_file_path + 'message_data.csv')

def setup(bot):
    bot.add_cog(Merit(bot))

