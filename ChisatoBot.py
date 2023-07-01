import json, os
import discord
from discord.ext import commands
import pathlib

# Commands path
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

    prefix = configData["prefix"]
    token = configData["token"]
    intents = discord.Intents.all()
    
    bot = commands.Bot(
        command_prefix = prefix,
        intents = intents,
        description = "ChisatoBot",
        activity = discord.Game(name = "Marumaru Galaxy"),
        status = discord.Status.online
    )

    # EVENTS

    @bot.event
    async def on_ready():
        print("El bot está listo para usarse.")

        # Loads files in commands folder
        for commandFile in COMMANDS_DIR.glob("*.py"):
            if commandFile.name != "__init__.py":
                await bot.load_extension(f"commands.{commandFile.name[:-3]}")

    bot.run(token)

if __name__ == '__main__':
    main()