import discord
import importlib, json, os
from dotenv import load_dotenv
from discord.ext import commands
from db import database
# import logging

# LOGGING

# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

class DecoratedAns():
    def __init__(self, title, description) -> None:
        self.title = title
        self.content = description

        self.ans = discord.Embed(
            title = self.title,
            description = self.content,
            colour = int("#E8053A", 16)
        )
    
    @property
    def send(self):
        return self.ans

def main():

    # Dotenv initialization
    load_dotenv()

    # Opens the configuration file if exists
    # Uses json.load(file)
    if os.path.exists('config.json'):
        with open('config.json') as config:
            configData = json.load(config)
    
    # Creates the json file if it doesn't exist
    # Uses json.dump(structure, file)
    else:
        template = {'prefix': 'c.'}
        with open('config.json', 'w') as config:
            json.dump(template, config)

    # BOT INITIALIZATION

    # TODO: Get prefix from the database
    prefix = configData["prefix"]
    token = os.getenv("TOKEN")
    intents = discord.Intents.all()
    
    bot = commands.Bot(
        command_prefix = prefix,
        intents = intents,
        description = "ChisatoBot",
        activity = discord.Game(name = "Marumaru Galaxy"),
        status = discord.Status.online
    )

    @bot.event
    async def on_ready():
        print("[CHISATO_BOT]: Iniciando bot...")

        # Database connection
        global connection
        connection = database.DBConnect()

        commands_dir = "./commands"

        # File loading from commands folder
        for folder in os.listdir(commands_dir):
            if os.path.isdir(os.path.join(commands_dir, folder)):
                for command_file in os.listdir(os.path.join(commands_dir, folder)):
                    if command_file.endswith(".py") and not command_file.startswith("__"):
                        module_name = f"commands.{folder}.{command_file[:-3]}"
                        try:
                            importlib.import_module(module_name)
                            await bot.load_extension(module_name)
                            print(f"[CHISATO_BOT]: Cargada extensión {module_name}.")
                        except Exception as e:
                            print(f"[CHISATO_BOT]: Error al cargar la extensión {command_file}: {e}.")

        print("[CHISATO_BOT]: El bot está listo para usarse.")

                
    # EVENTS

    @bot.event
    async def on_guild_join(guild):
        exists = database.VerifyServer(connection, guild)
        
        if exists:
            print(f"[CHISATO_BOT]: El servidor {guild.name} ya ha sido registrado anteriormente.")
            database.UpdateServer(connection, guild)
        else:
            database.RegisterServer(connection, guild)
            print(f"[CHISATO_BOT]: Se ha registrado el servidor {guild.name}.")
    
    @bot.event
    async def on_member_join(member: discord.Member):
        guild = member.guild

        # Add default role
        role = guild.get_role(1149530224791388282)
        await member.add_roles(role, reason = None, atomic = True)

        # If announcements channel exists
        if guild.system_channel is not None:
            await guild.system_channel.send(f"Welcome, {member.mention}!")

    # @bot.event
    # async def on_message(message):

    # @bot.event
    # async def on_reaction_add(reaction: discord.Reaction, user: discord.User):

    # Logging can enabled by setting the handler with log_handler = None
    bot.run(token = token)

if __name__ == '__main__':
    main()