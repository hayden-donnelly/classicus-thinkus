import discord
from discord.ext import commands
import pandas as pd
import plotly.express as px
from datetime import date
import global_vars as gv

class Merit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.merit_log = pd.read_csv(gv.hidden_file_path + 'test_data.csv', index_col='Date', parse_dates=True)
        except:
            self.merit_log = pd.DataFrame()

    def new_merit_log_entry(self, ctx, user_id):
        entry = {'Guild ID': ctx.message.guild.id, 'User ID': user_id, 
                'Merit': 1, 'Demerit': 0, 'Date': str(date.today())}
        self.merit_log = self.merit_log.append(entry, ignore_index=True)
        self.merit_log.to_csv(gv.hidden_file_path + 'test_data.csv')

    @commands.command()
    @commands.has_role("Admin")
    async def merit(self, ctx, user_id):
        self.new_merit_log_entry(ctx, user_id)
        await ctx.send("Merit point has been granted.")

    @commands.command()
    @commands.has_role("Admin")
    async def demerit(self, ctx, user_id):
        self.new_merit_log_entry(ctx, user_id)
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

def setup(bot):
    bot.add_cog(Merit(bot))

