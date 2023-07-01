import discord
from discord.ext import commands

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator = True)
    @commands.command(help = ".")
    async def ban(self, ctx):
        await ctx.reply("")

async def setup(bot):
    await bot.add_cog(Administration(bot))