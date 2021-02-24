import discord, pymongo
import datetime as dt
from discord.ext import commands
import settings

class listeners(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # Re-define the bot object into the class.

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

        # If the message author is not the bot itself or a bot user and the message is not a DM
        if (message.author.id != self.bot.user.id) and not (not message.guild) and (message.author.bot == False):
            user_query = {
                "userid":message.author.id,
                "serverid":message.guild.id
            }
            server_query = { "serverid": message.guild.id }
            if (settings.db.server_data.count_documents(server_query, limit = 1) != 1):
                # Create a new server entry if there is none
                template = {
                    "serverid":message.guild.id,
                    "msg_count":0,
                    "channel_blacklist":[],
                    "timestamp":dt.datetime.now()
                }
                settings.servercol.insert_one(template)
                await message.add_reaction("🆕")
            
            # If the message channel is blacklisted, stop.
            # Acquire server channel blacklist
            blacklist_doc = settings.servercol.find(server_query)
            for xy in blacklist_doc:
                if (message.channel.id in xy["channel_blacklist"]):
                    return

            # Otherwise, continue to create user entries and update message counts.
            server_doc = settings.servercol.find(server_query)
            for y in server_doc:
                settings.servercol.update_one(server_query,{"$set":{"msg_count":y["msg_count"] + 1}})

            if (settings.db.user_data.count_documents(user_query, limit = 1) != 1):
                # Create a new user entry if there is none
                template = {
                    "userid":message.author.id,
                    "serverid":message.guild.id,
                    "msg_count":1,
                    "timestamp": dt.datetime.now()
                }
                settings.usercol.insert_one(template)
                await message.add_reaction("✅")
            else:
                # Update the user's msg count if there is an entry
                doc = settings.usercol.find(user_query)
                for x in doc:
                    settings.usercol.update_one(user_query,{"$set":{"msg_count": x["msg_count"] + 1}})

            server_doc = settings.servercol.find(server_query)
            for z in server_doc:
                # Check for alerts

                # If there's an alert field, proceed.
                try:
                    alerts = z["alerts"]
                except:
                    return

                # If the alerts list is not empty:    
                if len(z["alerts"]) > 0:
                    # If the server's message count is the alert, send the alert.
                    if z["msg_count"] == alerts[0]:
                        alert_embed=discord.Embed(title="🎉 Alert Triggered", description=f"**{message.guild.name}** has hit **" + str(alerts[0]) + " messages**!", color=0x38fcf7)
                        alert_embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
                        alert_embed.set_footer(text="Made by http.james#6969")
                        await message.channel.send(embed=alert_embed)
                        # Delete the alert once it's triggered.
                        del alerts[0]
                        settings.servercol.update_one(server_query,{"$set":{"alerts":alerts}})

    @commands.Cog.listener('on_command_error')
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.CommandOnCooldown):
            # Avoid flooding the console when a command is spammed
            return
def setup(bot):
    bot.add_cog(listeners(bot))