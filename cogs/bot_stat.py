import discord
from datetime import datetime
from discord.ext import commands

class bot_stat(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # Re-define the bot object into the class.
    
    @commands.command(aliases=["latency"])
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def ping(self,ctx):
        await ctx.send(":ping_pong: API latency: **" + str(round(self.bot.latency*1000,2)) + " ms**.")
        await ctx.message.add_reaction('🏓')
    
    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def uptime(self,ctx):
        delta_uptime = datetime.now() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f":robot: I've been online for **{days} days**, **{hours} hours**, **{minutes} minutes** and **{seconds} seconds**.")
        await ctx.message.add_reaction('🤖')

def setup(bot):
    bot.add_cog(bot_stat(bot))