import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help = "Chisato te saludará.")
    async def hi(self, ctx):
        await ctx.reply('¡Wisu, wisu! ¿Necesitas algo de Chisato?')

async def setup(bot):
    await bot.add_cog(Utilities(bot))