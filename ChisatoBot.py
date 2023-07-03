import discord
import pathlib
import json, os
from dotenv import load_dotenv
from discord.ext import commands
from db import database

# DIRECTORIES

BASE_DIR = pathlib.Path("__file__").parent
COMMANDS_DIR = BASE_DIR / "commands"

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

        # File loading from commands folder
        for commandFile in COMMANDS_DIR.glob("*.py"):
            if commandFile.name != "__init__.py":
                await bot.load_extension(f"commands.{commandFile.name[:-3]}")

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

    bot.run(token)

if __name__ == '__main__':
    main()