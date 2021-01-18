import discord, pymongo, datetime, json
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
    'cogs.help'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    print("[Start] Cogs initialized")

myclient = pymongo.MongoClient(settings.configdata["mongo_url"])
db = myclient["chatboard"]
col = db["server_data"]
print("[Start] Databases linked")

usercol = db["user_data"]


@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(settings.configdata["token"])