import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # Re-define the bot object into the class.

    @commands.command(aliases=["help"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def cmds(self, ctx):
        embed=discord.Embed(title="Chatboard Help", description="Chatboard is a bot that keeps track of user chat activity. With a competitive leaderboard, this bot increases engagement and adds a competitive aspect to Discord communities.", color=0x8080ff)
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="Statistics", value="`cb?lb` - View the server leaderboard.\n`cb?user <user>` - Lookup another server member's message count.\n`cb?server` - View the server's message count.", inline=True)
        embed.add_field(name="Privacy", value="`cb?data` - View the data collected on you.\n`cb?data delete` - Initiate a data deletion request.", inline=True)
        embed.add_field(name="Administration", value="`cb?bl <#channel>` - Blacklist a channel from message counts.\n`cb?wl <#channel>` - Whitelist a blacklisted channel.\n`cb?reset` - Reset all server counts.", inline=True)
        embed.set_footer(text="Made by http.james#6969")
        try:
            await ctx.author.send(embed=embed)
        except:
            await ctx.send(f":x: I couldn't send you a DM, {ctx.author.mention}. Do you have DMs enabled?")
            return
        await ctx.send(f":white_check_mark: I sent you a DM, {ctx.author.mention}!")

def setup(bot):
    bot.add_cog(help(bot))