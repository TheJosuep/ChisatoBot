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
            raise MissingPermissions("Seems like you have not enough permissions to do that, huh?")
        return True
    return commands.check(predicate)

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help = "Ban a user: c.ban <user (mention) or ID> <delete messages (days) | optional> <reason | optional>")
    @has_ban_permissions()
    async def ban(self, ctx, users: commands.Greedy[discord.User] = None, deleteDays: typing.Optional[int] = 0,
                    *, reason: str = None):
        
        deleteSecs = deleteDays * 8640 # Days to seconds
        bannedMembers = []

        if users is None:
            await ctx.reply("You must enter at least one user!")
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
            await ctx.send(f"{membersMention} were banned from the server{givenReason}")
        elif len(bannedMembers) == 1:
            await ctx.send(f"{membersMention} was banned from the server{givenReason}")
        else:
            await ctx.send("An unexpected error has occurred...")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(error)

    @commands.command(help = "Shows bans list: c.bans")
    @has_ban_permissions()
    async def bans(self, ctx):
        
        await ctx.defer() # Defers the interaction due to a long task

        # Gets ban entries (contain an user and an optional reason)
        bans = [entry async for entry in ctx.guild.bans()]

        embed = discord.Embed(title = f"Ban list of {ctx.guild.name}.",
                              timestamp = datetime.now(),
                              color = discord.Colour.pink())
        
        # If server has banned people
        if len(bans) > 0:    
            for entry in bans:
                if len(embed.fields) > 25:
                    break
                if len(embed) > 5900:
                    embed.field(name = "Too many items in the list.")
                else:
                    embed.add_field(name = entry.user.name, value = f"User ID: {entry.user.id}. \nReason: {'Unspecified.' if entry.reason+'.' is None else entry.reason+'.'} \nBot: {'No.' if entry.user.bot is False else 'Yes.'}",
                                    inline = False)
            
            await ctx.reply(embed = embed)
        else:
            await ctx.reply("This server has no banned users.")
                
    @bans.error
    async def bans_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(error)

    @commands.command(help = "Unban a user: c.ban <user (mention) or ID> <reason | optional>")
    @has_ban_permissions()
    async def unban(self, ctx, users: commands.Greedy[discord.User] = None, *, reason: str = None):
        bannedUsers = [entry.user async for entry in ctx.guild.bans()]
        
        unbannedMembers = []
        nonbannedMembers = []

        if users is None:
            await ctx.reply("You must enter at least one user!")
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
                await ctx.send(f"{'Users '+errorMention+' were not found' if len(nonbannedMembers) > 1 else 'User '+errorMention+' was not found'} on the banned list.")

        # Validates the number of members banned and replies
        if len(unbannedMembers) > 1:
            await ctx.send(f"{membersMention} were unbanned from the server{givenReason}")
        elif len(unbannedMembers) == 1:
            await ctx.send(f"{membersMention} was unbanned from the server{givenReason}")
        else:
            await ctx.reply("This server has no banned users.")
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(error)

async def setup(bot):
    await bot.add_cog(Administration(bot))