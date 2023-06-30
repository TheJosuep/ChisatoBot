import json, os
import discord
from discord.ext import commands

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

    # Variables declaration
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

    @bot.command(name = "hi", help = "Chisato te saludará.")
    async def hi(ctx):
        await ctx.reply('¡Wisu, wisu! ¿Necesitas algo de Chisato?')

    bot.run(token)

if __name__ == '__main__':
    main()