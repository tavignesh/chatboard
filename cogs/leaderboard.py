import discord, pymongo
from discord.ext import commands
import settings

class leaderboard(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # Re-define the bot object into the class.

    # View the server leaderboard
    @commands.command(aliases=["leader"])
    @commands.cooldown(1,5,commands.BucketType.guild)
    async def lb(self,ctx):
        # Find the top 5 users in the user collection
        doc = settings.usercol.find({"serverid":ctx.guild.id}).sort("msg_count",-1).limit(5)
        leaderboard_list = []
        counter = 1
        for x in doc:
            user_obj = self.bot.get_user(x["userid"])
            leaderboard_list.append(str(counter) + ". " + user_obj.name + "#" + str(user_obj.discriminator) + " | " + str(x["msg_count"]))
            counter += 1
        if len(leaderboard_list) < 1:
                embed=discord.Embed(title="Leaderboard for " + ctx.guild.name, description="```No data to display.```", color=0x004080)
                embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator), icon_url=f"{ctx.author.avatar_url}")
                embed.set_footer(text="Made by http.james#6969")
                await ctx.send(embed=embed)
                return
        embed=discord.Embed(title="Leaderboard for " + ctx.guild.name, description="```" + '\n'.join(leaderboard_list) + "```", color=0x004080)
        embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator), icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text="Made by http.james#6969")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(leaderboard(bot))