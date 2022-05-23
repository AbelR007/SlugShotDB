import discord
from discord.ext import commands

class Admin_Options(commands.Cog,command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        hidden = False
    )
    @commands.is_owner()
    async def addslug(self, ctx, slugtypeid:str, type:str, rarity:str, attack:int, speed:int, *, slugname:str):
        user_id = int(ctx.message.author.id)

        await ctx.send("Send Image url :")

        def check(a):
            return a.author == ctx.message.author

        msg = await self.bot.wait_for('message', check=check)
        imgurl = str(msg.content)

        await ctx.send("Send Ghoul Version of slug :")
        ghoul_msg = await self.bot.wait_for('message', check=check)
        ghoul = str(ghoul_msg.content)

        await ctx.send("Send Description:")
        desc_msg = await self.bot.wait_for('message', check=check)
        desc = str(desc_msg.content)

        await ctx.send("Send Slug Emoji id:")
        emoji_msg = await self.bot.wait_for('message', check=check)
        slugemoji = str(emoji_msg.content)

        await self.bot.pg_con.execute(
            "INSERT INTO slugdata(slugtypeid, slugname, type, rarity,description, protoimgurl, ghoul, slugemoji, attack, speed) VALUES ($1, $2, $3, $4, $5,$6, $7, $8, $9, $10)",
            slugtypeid, slugname, type, rarity, desc, imgurl, ghoul, slugemoji, attack, speed)
        await ctx.send(f"Database registered successfully for {slugname}. Done.")

    @commands.command(
        hidden = True
    )
    @commands.is_owner()
    async def dbexecute(self, ctx, *, cmd):
        if int(ctx.message.author.id) != 636181565621141505:
            return await ctx.send("You are not worthy enough to use this command!")
        await self.bot.pg_con.execute(f"{cmd}")
        await ctx.send("Done.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dbfetch(self, ctx, *, cmd):
        if int(ctx.message.author.id) != 636181565621141505:
            return await ctx.send("You are not worthy enough to use this command!")
        data = await self.bot.pg_con.fetch(f"{cmd}")
        await ctx.send(data)

def setup(bot):
    bot.add_cog(Admin_Options(bot))
