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
    'cogs.controls'
]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    print("[Start] Cogs initialized")

myclient = pymongo.MongoClient(settings.configdata["mongo_url"])
db = myclient["chatboard"]
col = db["server_data"]
print("[Start] Databases linked")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def clear_s(ctx):
    col.delete_one({"serverid":ctx.guild.id})

@bot.command()
async def viewdb(ctx):
    doc = col.find()
    for x in doc:
        await ctx.send(x)
    otherdoc = db["user_data"].find()
    for i in otherdoc:
        await ctx.send(i)


bot.run(settings.configdata["token"])