import os

import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

import tasks
import functions


start = True
REGISTER_CHANNEL = 1007256114120904805
ADMIN_CHANNEL = 1007281390410285057
COVEN_CHANNEL = 1009098737529925815
HELP_CHANNEL = 1007626515351085077
me = 489412069620449280

PARTICIPANT_ID = 1007263717383217212
SQUIB_ID = 1007305614113906792
BOT_ID = 1006559803675525160
command_list = ["points"]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="",
            intents=discord.Intents.all(),
        )


bot = Bot()
load_dotenv()
TOKEN = os.getenv("TOKEN")


@bot.event
async def on_ready():
    print("Bot up and running")


@bot.event
async def on_message(ctx: discord.Message):
    if not ctx.author.bot:
        global start
        print(ctx.content)
        author = ctx.author
        content = ctx.content.lower()
        channel = ctx.channel
        data = content.split(" ")
        command = data[0]
        data = data[1:]
        data = ' '.join(data)
        if channel.id == REGISTER_CHANNEL:
            if functions.register(str(author.id)):
                role = get(ctx.guild.roles, id=PARTICIPANT_ID)
                await author.add_roles(role)
            await ctx.delete()
        elif channel.id == ADMIN_CHANNEL and command == "start":
            start = True
            print(start)
            await channel.send("Vazhojam")
        elif channel.id == COVEN_CHANNEL and command == "create":
            if data:
                if not functions.find_user(str(author.id)):
                    if await create_guild(ctx, data):
                        await channel.send("Hooray, you have successfully created a coven")
                    else:
                        await channel.send("Coven creation unsuccessful")
                else:
                    await channel.send("It seems that you are already in a coven. Leaving a coven leads to burning at the stake")
            else:
                await channel.send("You might have forgotten the coven name. The Command is \"create <coven_name>\"")
        elif channel.id == COVEN_CHANNEL and command == "join":
            if data:
                if not functions.find_user(str(author.id)):
                    result, memb = functions.join(str(author.id), data)
                    if result and memb:
                        role = get(ctx.guild.roles, name=data.lower())
                        if role:
                            await author.add_roles(role)
                    elif result:
                        await channel.send("It seems that this coven is full")
                else:
                    await channel.send("It seems that you are already in a coven. Leaving a coven leads to burning at the stake")
            else:
                await channel.send("You might have forgotten the coven name. The Command is \"join <coven_name>\"")
        elif not start and command in command_list:
            await channel.send("the event has not yet started")
        elif channel.id == HELP_CHANNEL and command == "points":
            try:
                if data:
                    guildname = " ".join(content.split(" ")[1:-1])
                    points = int(content.split(" ")[-1])
                    coven = functions.load_guild(guildname.lower())
                    coven.add_points(points, None)
                    functions.upload_guild(coven)
            except Exception as e:
                print("main" + str(e))
                await channel.send("points <coven> <number>")
        elif command == "answ":
            result = tasks.check_answer(str(author.id), data)
            if result:
                await channel.send(result)
                coven = functions.load_guild(functions.find_user(str(author.id)))
                if len(coven.completedTasks) < 24:
                    result = tasks.get_task(coven.currentTask)
                    await channel.send(embed=result)
                else:
                    embed = discord.Embed(title="Hooray", description="You have succesefully completed all the tasks")
                    await channel.send(embed=embed)
        elif command == "task":
            coven = functions.load_guild(functions.find_user(str(author.id)))
            result = tasks.get_task(coven.currentTask)
            await channel.send(embed=result)
        elif command == "hint":
            sub_channel = get(ctx.guild.channels, id=HELP_CHANNEL)
            await sub_channel.send("<@" + str(me) + "> help at <#" + str(channel.id) + ">")
        elif command == "lead":
            if channel.id == ADMIN_CHANNEL:
                result = functions.update_leaderboard()
                if result:
                    await channel.send(result)
            else:
                covenname = functions.find_user(str(author.id))
                coven = functions.load_guild(covenname)
                await channel.send(embed=coven.lead())
        elif command == "done":
            result = tasks.org_give_points(str(author.id), str(channel.id))
            if result:
                await channel.send(result)
                coven = functions.load_guild(functions.find_covenname_by_channelid(str(channel.id))) #i need to find the channel id and give that task, nes dabar duodu orgo id :)
                result = tasks.get_task(coven.currentTask)
                await channel.send(embed=result)
        elif command == "end":
            if author.id == me:
                result = functions.end_game(str(channel.id))
                if result:
                    await channel.send(result)
            else:
                sub_channel = get(ctx.guild.channels, id=HELP_CHANNEL)
                await sub_channel.send("<@" + str(me) + "> o coven want to end the game - <#" + str(channel.id) + ">")


async def create_guild(ctx, covenname):
    guild = ctx.guild
    member = ctx.author
    covenrole = await guild.create_role(name=covenname.lower(), colour=discord.Colour(0xd8ec14))
    squib = get(ctx.guild.roles, id=SQUIB_ID)
    await member.add_roles(covenrole)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        covenrole: discord.PermissionOverwrite(read_messages=True),
        squib: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(covenname, overwrites=overwrites)
    functions.create_guild(covenname, str(member.id), channel.id)
    return True


bot.run(TOKEN)
