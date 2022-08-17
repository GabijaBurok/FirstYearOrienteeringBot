import json
import random
from datetime import datetime

import discord

import functions

TASKS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
last_update = "00:00"


class Coven:
    def __init__(self, uid, channelid=None, name="none", start=str(datetime.now()), points=0, currentTask=1, completedTasks=[], end=str(datetime.now())):
        self.members = uid
        self.channelid = channelid
        self.name = name
        self.start = start
        self.points = points
        self.currentTask = currentTask
        self.completedTasks = completedTasks
        self.end = end

    def __repr__(self):
        string = "**_" + self.name + "_**\n"
        for member in self.members:
            string += "<@" + str(member) + ">\n"
        string += "Total Coven Points: " + str(self.points)
        string += "\n Mischieves managed: " + str(len(self.completedTasks))
        return string

    def new_member(self, uid):
        if len(self.members) < 5:
            self.members.append(uid)
            return True
        else:
            return False

    def add_points(self, points):
        self.points += points
        with open("covenList.json", "r+") as f:
            data = json.load(f)
            data[self.name] += points
            f.seek(0)
            f.truncate()
            json.dump(data, f)
            return True

    def give_next(self):
        self.completedTasks.append(self.currentTask)
        if self.currentTask == 24:
            self.currentTask = 1
        else:
            self.currentTask += 1

    def lead(self):
        try:
            with open("leaderboard.json", "r") as f:
                data = json.load(f)[self.name.lower()]
                embed = discord.Embed(title="Latest leaderboards:")
                for i in range(1, len(data)):
                    embed.add_field(name=data[-i][0], value="Points collected: " + str(data[-i][1]), inline=False)
                embed.set_footer(text="Last update "+last_update)
                return embed
        except Exception as e:
            print("functions" + str(e))
            return discord.Embed(title="Leaderboard is not prepared yet. Try again later", description="We update leaderboards every 30 minutes")

    def end_game(self):
        self.end = str(datetime.now())
        return True


def register(uid):
    with open("participants.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        if uid not in data.keys():
            data.update({uid: None})
            f.seek(0)
            f.truncate()
            json.dump(data, f)
            return True
        else:
            return False


def find_user(uid):
    with open("participants.json", "r") as f:
        data = json.load(f)
        if uid in data:
            return data[uid]
        else:
            return None


def find_covenname_by_channelid(cid):
    with open("covenChannels.json", "r") as f:
        data = json.load(f)
        if cid in data:
            return data[cid]
        else:
            return None


def set_guild(uid, covenname):
    with open("participants.json", "r+") as f:
        data = json.load(f)
        if covenname:
            data[uid] = covenname.lower()
        else:
            data[uid] = None
        f.seek(0)
        f.truncate()
        json.dump(data, f)


def choosestart():
    start = random.choice(TASKS)
    TASKS.remove(start)
    return start


def create_guild(covenname, uid, channelid):
    with open("covenList.json", "r+") as covens:
        data = json.load(covens)
        if covenname not in data.keys():
            with open("covens/" + covenname.lower() + ".json", "w+") as coven:
                json.dump(Coven(name=covenname, uid=[uid], channelid=channelid, currentTask=choosestart()).__dict__, coven, indent=4)
            data.update({covenname: 0})
            covens.seek(0)
            covens.truncate()
            json.dump(data, covens, indent=4)
            set_guild(uid, covenname.lower())
            with open("covenChannels.json", "r+") as f:
                data2 = json.load(f)
                data2.update({channelid: covenname})
                f.seek(0)
                f.truncate()
                json.dump(data2, f, indent=4)
            return True
        else:
            return False


def load_guild(guildname):
    with open("covens/" + guildname.lower() + ".json", "r") as f:
        lst = json.load(f).values()
        data = Coven(*lst)
        return data


def upload_guild(guild):
    with open("covens/" + guild.name.lower() + ".json", "r+") as f:
        data = guild.__dict__
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)


def join(uid, guildname):
    try:
        guild = load_guild(guildname)
        if not guild:
            return False
        memb = guild.new_member(uid)
        if memb:
            set_guild(uid, guildname)
            upload_guild(guild)
        return True, memb
    except Exception as e:
        print(str(e) + " while joining guild")
        return False, True


def update_leaderboard():
    with open("covenList.json", "r") as f:
        data = json.load(f)
    sorted_data = sorted(data.items(), key=lambda x: x[1])
    with open("leaderboard.json", "w") as ff:
        new_data = {}
        end = len(sorted_data)
        for i in range(0, end):
            listas = []
            if i >= 2:
                listas.append(sorted_data[i - 2])
            if i >= 1:
                listas.append(sorted_data[i - 1])
            listas.append(sorted_data[i])
            if i < end - 1:
                listas.append(sorted_data[i + 1])
            if i < end - 2:
                listas.append(sorted_data[i + 2])
            new_data[sorted_data[i][0]] = listas
        json.dump(new_data, ff, indent=4)

    now = datetime.now()
    global last_update
    last_update = now.strftime("%H:%M")
    result = ""
    for i in range(1, end):
        result += "No." + str(i) + " " + sorted_data[len(sorted_data) - i][0] + " " + str(
            sorted_data[len(sorted_data) - i][1]) + "\n"
    return result


def end_game(cid):
    covenname = functions.find_covenname_by_channelid(cid)
    coven = functions.load_guild(covenname)
    result = coven.end_game()
    if result:
        functions.upload_guild(coven)
        return "You have sucessefuly completed the game"
    print(":)")

