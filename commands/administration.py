import discord, typing
from discord.ext import commands
from datetime import datetime

# CHECKS

class MissingPermissions(commands.CheckFailure):
    pass

# Check if the user trying to ban has a higher role than the other member
def higher_hierarchy(ctx, member):
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
            await ctx.send(f"{membersMention} fueron baneados{givenReason}")
        elif len(bannedMembers) == 1:
            await ctx.send(f"{membersMention} fue baneado{givenReason}")
        else:
            await ctx.reply("¡Debes mencionar al menos a un miembro!")
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(error)
    
    @commands.command(help = "Muestra la lista de usuarios baneados.")
    @has_ban_permissions()
    async def bans(self, ctx):
        # Defers the interaction due to a long task
        await ctx.defer()
        # Gets the ban entries that contains an user and a reason (optional)
        bans = [entry async for entry in ctx.guild.bans()]

        embed = discord.Embed(title = f"Usuarios baneados de {ctx.guild.name}.",
                              timestamp = datetime.now(),
                              color = discord.Colour.pink())
        if len(bans) > 0:    
            for entry in bans:
                if len(embed.fields) > 25:
                    break
                if len(embed) > 5900:
                    embed.field(name = "Demasiados elementos en la lista.")
                else:
                    embed.add_field(name = entry.user.name, value = f"ID del usuario: {entry.user.id} \nRazón: {'Sin especificar.' if entry.reason is None else entry.reason} \nBot: {'No' if entry.user.bot is False else 'Sí'}",
                                    inline = False)
            
            await ctx.reply(embed = embed)
        else:
            await ctx.reply("No hay usuarios baneados en el servidor.")
                

    @commands.command(help = "Quita el ban a un usuario: c.ban <usuario>")
    @has_ban_permissions()
    async def unban(self, ctx, user = None, *, reason: str = None):
        bannedUsers = [entry async for entry in ctx.guild.bans()]
        givenReason = '.' if reason == None else ' por ' + reason + '.'

        if user is None:
            ctx.reply("Debe ingresar un nombre o el id de un usuario.")
        else:
            if isinstance(user, int):
                for bannedUser in bannedUsers:
                    if bannedUser.user.id == user:
                        await bannedUser.unban(bannedUser, reason)
                        await ctx.send(f"El usuario {bannedUser.user.name} fue desbaneado{givenReason}")
                
                ctx.reply("El usuario no ha sido encontrado en la lista de baneados.")

async def setup(bot):
    await bot.add_cog(Administration(bot))