import discord, pymongo
from discord.ext import commands
import settings

class admin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # Re-define the bot object into the class.
    
    myclient = pymongo.MongoClient(settings.configdata["mongo_url"])
    db = myclient["chatboard"]
    servercol = db["server_data"]
    usercol = db["user_data"]

    @commands.command(aliases=["bl"])
    @commands.has_permissions(manage_channels=True)
    async def blacklist(self,ctx,channel: discord.TextChannel):
        # Blacklist a server text channel
        server_query = {"serverid":ctx.guild.id}
        server_doc = self.servercol.find(server_query)
        for x in server_doc:
            # If the desired text channel is already blacklisted, do nothing.
            if (channel.id in x["channel_blacklist"]):
                await ctx.send(":warning: This channel is already blacklisted.")
                return
            # Otherwise, update the document as normal.
        
            blacklist = x["channel_blacklist"]
            blacklist.append(channel.id)
            self.servercol.update_one(server_query,{"$set":{"channel_blacklist":blacklist}})
            await ctx.send(":white_check_mark: Channel successfully blacklisted.")
    
    @commands.command(aliases=["wl"])
    @commands.has_permissions(manage_channels=True)
    async def whitelist(self,ctx,channel: discord.TextChannel):
        # Whtielist a server text channel
        server_query = {"serverid":ctx.guild.id}
        server_doc = self.servercol.find(server_query)
        for x in server_doc:
            # If the desired text channel is already whitelisted, do nothing.
            if (channel.id not in x["channel_blacklist"]):
                await ctx.send(":warning: This channel is already whitelisted.")
                return
            # Otherwise, update the document as normal.

            blacklist = x["channel_blacklist"]
            blacklist.remove(channel.id)
            self.servercol.update_one(server_query,{"$set":{"channel_blacklist":blacklist}})
            await ctx.send(":white_check_mark: Channel successfully whitelisted.")

def setup(bot):
    bot.add_cog(admin(bot))