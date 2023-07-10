import discord, typing
from discord.ext import commands

# CHECKS

class MissingPermissions(commands.CheckFailure):
    pass

# Check if the user trying to ban has a higher role than the other member
def ban_permissions(ctx, member):
    return ctx.author.top_role > member.top_role

# Check if
def has_ban_permissions():
    async def predicate(ctx):
        if ctx.author.guild_permissions.ban_members is False:
            raise MissingPermissions("Parece que no tienes permisos suficientes para esto~.")
        return True
    return commands.check(predicate)

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help = "Banea a un usuario: c.ban <usuario> <borrar mensajes (días) | opcional> <razón | opcional>")
    @has_ban_permissions()
    async def ban(self, ctx, members: commands.Greedy[discord.Member], deleteDays: typing.Optional[int] = 0,
                   *, reason: str = None):
        
        deleteSecs = deleteDays * 8640 # Parses days to seconds
        bannedMembers = []

        for member in members:
            await member.ban(delete_message_seconds = deleteSecs, reason = reason)
            bannedMembers.append(member.mention)

        membersMention = ', '.join(bannedMembers) # Joins the member's mention in a new variable to print it easier
        givenReason = '.' if reason is None else ' por ' + reason + '.'

        if len(bannedMembers) > 1:
            await ctx.reply(f"{membersMention} fueron baneados{givenReason}")
        elif len(bannedMembers) == 1:
            await ctx.reply(f"{membersMention} fue baneado{givenReason}")
        else:
            await ctx.send("¡Debes mencionar al menos a un miembro!")
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(error)
    
    @commands.has_permissions(administrator = True)
    @commands.command(help = "Desbanea a un usuario")
    async def unban(ctx, *, member):
        bannedUsers = await ctx.guild.bans()

async def setup(bot):
    await bot.add_cog(Administration(bot))