import discord, pymongo
import datetime as dt
from discord.ext import commands
import settings

class listeners(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # Re-define the bot object into the class.

    myclient = pymongo.MongoClient(settings.configdata["mongo_url"])
    db = myclient["chatboard"]
    servercol = db["server_data"]
    usercol = db["user_data"]

    # When the bot logs in, print bot details to console
    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        print('[BOOT] Logged in at ' + str(dt.datetime.now()))
        await self.bot.change_presence(activity=discord.Game(name="cb?help"))
        print("[INFO] Username:",self.bot.user.name)
        print("[INFO] User ID:",self.bot.user.id)

    # When a message is detected, do X
    @commands.Cog.listener('on_message')
    async def on_message(self,message):

        # If the message author is not the bot itself and the message is not a DM
        if (message.author.id != self.bot.user.id) and not (not message.guild):
            user_query = {
                "userid":message.author.id,
                "serverid":message.guild.id
            }
            server_query = { "serverid": message.guild.id }
            if (self.db.server_data.count_documents(server_query, limit = 1) != 1):
                # Create a new server entry if there is none
                template = {
                    "serverid":message.guild.id,
                    "msg_count":0,
                    "channel_blacklist":[],
                    "timestamp":dt.datetime.now()
                }
                self.servercol.insert_one(template)
                await message.add_reaction("🆕")
                print("Server inserted.")
            
            # If the message channel is blacklisted, stop.
            # Acquire server channel blacklist
            blacklist_doc = self.servercol.find(server_query)
            for xy in blacklist_doc:
                if (message.channel.id in xy["channel_blacklist"]):
                    return
            # Otherwise, continue to create user entries and update message counts.
            server_doc = self.servercol.find(server_query)
            for y in server_doc:
                self.servercol.update_one(server_query,{"$set":{"msg_count":y["msg_count"] + 1}})
            if (self.db.user_data.count_documents(user_query, limit = 1) != 1):
                # Create a new user entry if there is none
                template = {
                    "userid":message.author.id,
                    "serverid":message.guild.id,
                    "msg_count":1,
                    "timestamp": dt.datetime.now()
                }
                self.usercol.insert_one(template)
                await message.add_reaction("✅")
                print("User inserted")
            else:
                # Update the user's msg count if there is an entry
                doc = self.usercol.find(user_query)
                for x in doc:
                    self.usercol.update_one(user_query,{"$set":{"msg_count": x["msg_count"] + 1}})


def setup(bot):
    bot.add_cog(listeners(bot))