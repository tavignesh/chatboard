import discord, datetime, json
from discord.ext import commands

# Import config info
import settings

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix=settings.configdata["prefix"],intents=intents)
bot.remove_command('help')
bot.launch_time = datetime.datetime.now()
print("[Start] Launch time defined")

initial_extensions = [
    'cogs.listeners',
    'cogs.admin',
    'cogs.lookup',
    'cogs.leaderboard',
    'cogs.controls',
    'cogs.help',
    'cogs.bot_stat'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    print("[Start] Cogs initialized")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(settings.configdata["token"])