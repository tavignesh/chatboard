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
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1,20,commands.BucketType.user)
    async def reset(self,ctx):
        # Server reset embed
        embed=discord.Embed(title="Server Reset Request", description=f"Are you sure you want to reset **{ctx.guild.name}**'s message counts? This will set both the server's global and your members' message counts to 0 irreversibly.", color=0xff0000)
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="To proceed, react with ✅", value="To abort react with ❌", inline=True)
        embed.set_footer(text="Made by http.james#6969")
        reset = await ctx.send(embed=embed)
        # Add interactive reactions
        await reset.add_reaction('✅')
        await reset.add_reaction('❌')

        # Define the callback function that waits for reactions.
        def check(reaction,user):
            return str(reaction.emoji) in ['✅','❌'] and user == ctx.author
        try:# Run callback sequence
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:# Request timed out, abort and alert user.
            await reset.delete()
            await ctx.send("Request timed out. No data has been deleted")
        else:
            # If the user reacts with the check mark emoji, delete the server's data.
            if str(reaction.emoji) == "✅":
                # Reset confirmation embed
                embed=discord.Embed(title="Resetting...", description="We're currently resetting the server's statistics. Please wait...", color=0xffff00)
                embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text="Made by http.james#6969")
                # Edit the first embed
                await reset.edit(embed=embed)
                # Delete the server document from the server collection
                self.servercol.delete_many({"serverid":ctx.guild.id})
                # Progress update embed
                embed=discord.Embed(title="Resetting...", description="We're currently resetting the server's statistics. Please wait...\n\n**(50%)** Server document deleted.", color=0xffff00)
                embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text="Made by http.james#6969")
                # Edit the first embed
                await reset.edit(embed=embed)
                # Delete the server members' documents from the user data collection
                self.usercol.delete_many({"serverid":ctx.guild.id})
                # Final reset confirmation embed
                embed=discord.Embed(title="Reset Successful", description="We've successfully reset all server statistics.", color=0x008000)
                embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text="Made by http.james#6969")
                # Edit the first embed
                await reset.edit(embed=embed)
                return
            # If the user reacts with the X, abort and notify the user.
            embed=discord.Embed(title="Aborted", description="No data has been reset.", color=0xff8080)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text="Made by http.james#6969")
            # Edit the first embed
            await reset.edit(embed=embed)

def setup(bot):
    bot.add_cog(admin(bot))