import discord
from discord.ext import commands
import asyncio

# Check if the user trying to ban has a higher role than the other member
def ban_permissions(ctx, member):
    return ctx.author.top_role > member.top_role

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(ban_members = True)
    @commands.command(help = "Banea a un usuario: c.ban <usuario> <razón>")
    async def ban(ctx, member: discord.Member, *, reason = None):
        if not ban_permissions(ctx, member):
            await ctx.reply("No cuentas con los suficientes permisos para hacer esto.")
            return
        
        await ctx.guild.ban(member, reason)
        
        if reason is None:
            await ctx.send(f"El miembro {member} fue baneado.")
        else:
            await ctx.send(f"El miembro {member} fue baneado por {reason}.")
    
    @commands.has_permissions(administrator = True)
    @commands.command(help = "Desbanea a un usuario")
    async def unban(ctx, *, member):
        bannedUsers = await ctx.guild.bans()

async def setup(bot):
    await bot.add_cog(Administration(bot))