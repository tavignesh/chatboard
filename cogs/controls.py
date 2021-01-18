import discord, pymongo, asyncio
from datetime import datetime
from discord.ext import commands
import settings

class controls(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # Re-define the bot object into the class.

    myclient = pymongo.MongoClient(settings.configdata["mongo_url"])
    db = myclient["chatboard"]
    servercol = db["server_data"]
    usercol = db["user_data"]

    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)
    async def data(self,ctx,parameters=None):
        # This is the command for users to manage the data collected on them.
        # It allows them to view data stored and delete it on request.

        # View data
        if parameters == None or parameters == "view":
            # Search for the user in the user collection and strip the internal ID
            userdoc = self.usercol.find({"userid":ctx.author.id,"serverid":ctx.guild.id},{"_id":0})
            for x in userdoc:
                # Attempt to send the user a DM with their data.
                # If the bot fails to send, alert the user. Otherwise, proceed like normal.
                try:
                    await ctx.author.send(f":wave: Hi **{ctx.author.name}**! You're receiving this message because you requested your data at **" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + f"**. Here's all the data we store on you in **{ctx.guild.name}** server.\n\n```" + str(x) + "```")
                except:
                    await ctx.send(f":x: I couldn't send you a DM, {ctx.author.mention}. Do you have DMs enabled?")
                    return
                await ctx.send(f":white_check_mark: Check your DMs, {ctx.author.mention}.")
        elif parameters == "delete":
            # Allows the user to delete the data stored on them permanently.
            embed=discord.Embed(title="Data Deletion Request", description=f"Are you sure you want to delete **ALL DATA** stored about you in {ctx.guild.name}? This will permanently reset your message count.", color=0xff0000)
            embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator), icon_url=f"{ctx.author.avatar_url}")
            embed.add_field(name="To proceed, react with ✅", value="If you'd like to abort, react with ❌", inline=False)
            embed.set_footer(text="Made by http.james#6969")
            # Attempt to send the user a DM to delete their data.
            # If the bot fails to send, alert hte user. Otherwise, proceed like normal.
            try:
                deletion = await ctx.author.send(embed=embed)
            except:
                await ctx.send(f":x: I couldn't send you a DM, {ctx.author.mention}. Do you have DMs enabled?")
                return
            # Add interactive reactions.
            await deletion.add_reaction('✅')
            await deletion.add_reaction('❌')
            await ctx.send(f":white_check_mark: Check your DMs, {ctx.author.mention}.")
            # Define the callback function that waits for reactions.
            def check(reaction,user):
                return str(reaction.emoji) in ['✅','❌'] and user == ctx.author
            try:# Run callback sequence
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:# Request timed out, abort and alert user.
                await deletion.delete()
                await ctx.send("Request timed out. No data has been deleted")
            else:
                # If the user reacts with the check mark emoji, delete their data.
                if str(reaction.emoji) == "✅":
                    self.usercol.delete_many({"userid":ctx.author.id,"serverid":ctx.guild.id})
                    embed=discord.Embed(title="Data Deleted", description=f"**ALL DATA** about you within {ctx.guild.name} has been permanently erased.", color=0x008000)
                    embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator), icon_url=f"{ctx.author.avatar_url}")
                    embed.set_footer(text="Made by http.james#6969")
                    # Edit the embed
                    await deletion.edit(embed=embed)
                    return
                # If the user reacts with the X emoji, abort.
                embed=discord.Embed(title="Data Kept", description="You aborted, so no data was deleted.", color=0xffff00)
                embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator), icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text="Made by http.james#6969")
                # Edit the embed
                await deletion.edit(embed=embed)

def setup(bot):
    bot.add_cog(controls(bot))