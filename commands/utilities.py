import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help = "Chisato te saludará.")
    async def hi(self, ctx):
        await ctx.reply('¡Wisu, wisu! ¿Necesitas algo de Chisato?')

    @commands.command(help = "Chisato dirá algo por ti: c.say <texto>")
    async def say(self, ctx, *, text: str = None):
        if text is not None:
            await ctx.send(text)
            await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(Utilities(bot))