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

    @commands.command(help = "Banea a un usuario: c.ban <usuario (mención) o ID> <borrar mensajes (días) | opcional> <razón | opcional>")
    @has_ban_permissions()
    async def ban(self, ctx, users: commands.Greedy[discord.User] = None, deleteDays: typing.Optional[int] = 0,
                   *, reason: str = None):
        
        deleteSecs = deleteDays * 8640 # Days to seconds
        bannedMembers = []

        if users is None:
            await ctx.reply("¡Debes ingresar al menos a un usuario!")
            return
        else:
            for user in users:
                # Verifies if the user is in the current server
                member = ctx.guild.get_member(user.id)

                # Mentions the user if is in the server, otherwise just append the name
                if member is not None:
                    bannedMembers.append(member.mention)
                else:
                    bannedMembers.append(user.name)
                
                await ctx.guild.ban(user = user, delete_message_seconds = deleteSecs, reason = reason)

        # Converts members mention and given reason in new variables for easier printing
        if len(bannedMembers) > 1:
            membersMention = ', '.join(bannedMembers[:-1]) + ' y ' + bannedMembers[-1]
        elif len(bannedMembers) > 0:
            membersMention = bannedMembers[0]

        givenReason = '.' if reason is None else ' por ' + reason + '.'

        # Validates the number of members banned and replies
        if len(bannedMembers) > 1:
            await ctx.send(f"{membersMention} fueron baneados del servidor{givenReason}")
        elif len(bannedMembers) == 1:
            await ctx.send(f"{membersMention} fue baneado del servidor{givenReason}")
        else:
            await ctx.send("Un error inesperado ha ocurrido...")
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(error)
    
    @commands.command(help = "Muestra la lista de usuarios baneados.")
    @has_ban_permissions()
    async def bans(self, ctx):
        
        await ctx.defer() # Defers the interaction due to a long task

        # Gets ban entries (contain an user and an optional reason)
        bans = [entry async for entry in ctx.guild.bans()]

        embed = discord.Embed(title = f"Usuarios baneados de {ctx.guild.name}.",
                              timestamp = datetime.now(),
                              color = discord.Colour.pink())
        
        # If server has banned people
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
                

    @commands.command(help = "Remueve el ban de un usuario: c.ban <usuario> <razón | opcional>")
    @has_ban_permissions()
    async def unban(self, ctx, users: commands.Greedy[discord.User] = None, *, reason: str = None):
        bannedUsers = [entry.user async for entry in ctx.guild.bans()]
        
        unbannedMembers = []
        nonbannedMembers = []

        if users is None:
            await ctx.reply("¡Debes ingresar al menos a un usuario!")
        else:
            for user in users:
                if len(bannedUsers) > 0:
                    for bannedUser in bannedUsers:
                        if bannedUser == user:
                            unbannedMembers.append(user.name)
                            await ctx.guild.unban(bannedUser)
                        else:
                            nonbannedMembers.append(user.name)
            
        # Converts members mention and given reason in new variables for easier printing
        if len(unbannedMembers) > 1:
            membersMention = ', '.join(unbannedMembers[:-1]) + ' y ' + unbannedMembers[-1]
        elif len(unbannedMembers) > 0:
            membersMention = unbannedMembers[0]

        if len(nonbannedMembers) > 1:
            errorMention = ', '.join(nonbannedMembers[:-1]) + ' y ' + nonbannedMembers[-1]
        elif len(nonbannedMembers) > 0:
            errorMention = nonbannedMembers[0]

        givenReason = '.' if reason == None else ' por ' + reason + '.'

        if len(nonbannedMembers) > 0:
                await ctx.send(f"{'Los usuarios '+errorMention+' no fueron encontrados' if len(nonbannedMembers) > 1 else 'El usuario '+errorMention+' no fue encontrado'} en la lista de baneados.")

        # Validates the number of members banned and replies
        if len(unbannedMembers) > 1:
            await ctx.send(f"{membersMention} fueron desbaneados del servidor{givenReason}")
        elif len(unbannedMembers) == 1:
            await ctx.send(f"{membersMention} fue desbaneado del servidor{givenReason}")
        else:
            await ctx.reply("No hay usuarios baneados en el servidor.")

async def setup(bot):
    await bot.add_cog(Administration(bot))