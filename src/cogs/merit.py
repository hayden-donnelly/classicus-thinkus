import discord
from discord.ext import commands
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns

class Merit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.merit_log = pd.read_csv('../../test_data.csv')
        except:
            self.merit_log = pd.DataFrame()

    def new_merit_log_entry(self, ctx, user_id):
        entry = {'Guild ID': ctx.message.guild.id, 'User ID': user_id, 
                'Merit': 1, 'Demerit': 0, 'Date': str(date.today())}
        self.merit_log = self.merit_log.append(entry, ignore_index=True)
        self.merit_log.to_csv('../../test_data.csv')

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
    async def merit_history(self, ctx):
        data = pd.DataFrame(self.merit_log.groupby('Date', as_index=False)['Merit'].count())
        data = pd.DataFrame({'Date': data['Date'], 'Merit': data['Merit']})
        plot = sns.lineplot(data=data, x ='Date', y='Merit')
        plt.xticks(rotation=20)
        plt.rcParams['savefig.dpi'] = 300
        plot.get_figure().savefig('../../merit_history.png')
        plot.get_figure().clf()
        await ctx.send(file=discord.File('../../merit_history.png'))

def setup(bot):
    bot.add_cog(Merit(bot))

