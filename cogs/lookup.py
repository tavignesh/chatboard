import discord, pymongo
from datetime import datetime
from discord.ext import commands
import settings

class lookup(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # Re-define the bot object into the class.

    myclient = pymongo.MongoClient(settings.configdata["mongo_url"])
    db = myclient["chatboard"]
    servercol = db["server_data"]
    usercol = db["user_data"]

    @commands.command()
    @commands.cooldown(1,3,commands.BucketType.user)
    async def user(self,ctx,user:discord.Member = None):
        # If there is no user input, default to the user.
        if user == None:
            user = ctx.author
        # View a user's stats in the same server.
        doc = settings.usercol.find({"userid":user.id,"serverid":ctx.guild.id})
        for x in doc:
            time = x["timestamp"].strftime("%m/%d/%Y, %H:%M:%S")
            embed=discord.Embed(title=user.name + "#" + str(user.discriminator), color=0x008080)
            embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator), icon_url=f"{ctx.author.avatar_url}")
            embed.add_field(name="Info", value="**Message Count**: " + str(x["msg_count"]) + "\n**First Message**: " + str(time), inline=False)
            embed.set_footer(text="Made by http.james#6969")
            await ctx.send(embed=embed)
    
    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def server(self,ctx):
        # View the server's global stats.
        doc = settings.servercol.find({"serverid":ctx.guild.id})
        for x in doc:
            time = x["timestamp"].strftime("%m/%d/%Y, %H:%M:%S")
            embed=discord.Embed(title=ctx.guild.name, color=0xBB4411)
            embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator), icon_url=f"{ctx.author.avatar_url}")
            embed.add_field(name="Info", value="**Message Count**: " + str(x["msg_count"]) + "\n**First Message**: " + str(time), inline=False)
            embed.set_footer(text="Made by http.james#6969")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(lookup(bot))