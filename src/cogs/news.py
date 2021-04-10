import discord
from discord.ext import commands
import nltk
from newspaper import Article
import global_vars as gv

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def summarize(self, ctx, article_url):
        article = Article(article_url)
        article.download()
        article.parse()
        article.nlp()

        embed = discord.Embed(title=article.title, url=article_url)
        embed.set_image(url=article.top_image)
        embed.add_field(name="Summary", value=article.summary)
        await ctx.send(embed=embed)
        await gv.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(News(bot))