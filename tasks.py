import discord
import json
import functions


class Task:
    lead: object

    def __init__(self, id, name, lead, person, task, answer, spot_reward, reward):
        self.id = id
        self.name = name
        self.lead = lead
        self.person = person
        self.task = task
        self.answer = answer
        self.spot_reward = spot_reward
        self.reward = reward


def check_answer(uid, answer):
    covenname = functions.find_user(uid)
    coven = functions.load_guild(covenname)
    with open("tasks.json", "r") as t:
        data = json.load(t)
        if answer in data.keys():
            task = Task(*data[answer].values())
            if coven.currentTask == task.id:
                result = coven.add_points(task.reward)
                coven.give_next()
                functions.upload_guild(coven)
                if len(coven.completedTasks) >= 24:
                    return "You have completed " + str(task.name) + "\nReward of " + str(task.reward) + " points has been given \n"
                if result:
                    return "You have completed " + str(task.name) + "\nReward of " + str(task.reward) + " points has been given \nYour next task is"
            else:
                return "This is not the correct answer"
        else:
            return "This is not the correct answer"


def org_give_points(uid, cid):
    with open("covenChannels.json", "r") as f:
        data = json.load(f)
        if cid in data.keys():
            covenname = data[cid]
            coven = functions.load_guild(covenname)
            tid, name, points = org_dict[uid].values()
            if coven.currentTask == tid:
                result = coven.add_points(points)
                if result:
                    coven.give_next()
                    functions.upload_guild(coven)
                    return "You have completed " + str(name) + "\nReward of " + str(
                        points) + " points has been given \nYour next task is"
                return "Add Points"
            else:
                return "This is not the correct answer"
        else:
            print("something is wrong :)")


def get_task(currenttask):
    for t in task_dict:
        if t.id == currenttask:
            embed = discord.Embed(title=t.name, description=t.lead)
            return embed


task_dict = {
    Task(1, "The High Priestess", "Gabriel?? Vilutyt??", "lead", "task", "answer", 10, 10),
    Task(2, "The Chariot", "lead", "Fausta", "task", "answer", 10, 10),
    Task(3, "The Star", "lead", "Agota", "task", "answer", 10, 10),
    Task(4, "The Emperor", "lead", "M??ta", "task", "answer", 10, 10),
    Task(5, "Pentacles", "lead", "Lau??aviet??", "task", "answer", 10, 10),
    Task(6, "The Empress", "lead", "Gabriel?? Kasperait??", "task", "answer", 10, 10),
    Task(7, "The Sun", "lead", "Titas", "task", "answer", 10, 10),
    Task(8, "The Fool", "lead", "Adomas", "task", "answer", 10, 10),
    Task(9, "Wheel Of Fortune", "lead", "Ugn?? Petrauskait??", "task", "answer", 10, 10),
    Task(10, "Justice", "lead", "Agn??", "task", "answer", 10, 10),
    Task(11, "Wands", "lead", "Med??iai", "task", "answer", 10, 10),
    Task(12, "The Devil", "lead", "Augustina", "task", "answer", 10, 10),
    Task(13, "The Lovers", "lead", "Paulina ir Darius", "task", "answer", 10, 10),
    Task(14, "The Tower", "lead", "Nojus", "task", "answer", 10, 10),
    Task(15, "Swords", "lead", "V??liavos", "task", "answer", 10, 10),
    Task(16, "The Hierophant", "lead", "Viktorija", "task", "answer", 10, 10),
    Task(17, "Temperance", "lead", "Lukas", "task", "answer", 10, 10),
    Task(18, "Judgement", "lead", "Greta Grigait??", "task", "answer", 10, 10),
    Task(19, "The Magician", "lead", "Ugn?? Me??kuotyt??", "task", "answer", 10, 10),
    Task(20, "Cups", "lead", "Snacks?? zona", "task", "answer", 10, 10),
    Task(21, "The Hermit", "lead", "Gabija", "task", "answer", 10, 10),
    Task(22, "The Moon", "lead", "Domas", "task", "answer", 10, 10),
    Task(23, "The World", "lead", "Mantas", "task", "answer", 10, 10),
    Task(24, "Strength", "lead", "Anastasija", "task", "answer", 10, 10)
}

org_dict = {
    "597042345774678016":
        {
            "id": 1,
            "name": "The High Priestess",
            "points": 10
        },
    "881266661775245423":
        {
            "id": 2,
            "name": "The Chariot",
            "points": 10
        },
    "430444847053275137":
        {
            "id": 3,
            "name": "The Star",
            "points": 10
        },
    "M??ta":
        {
            "id": 4,
            "name": "The Emperor",
            "points": 10
        },
    "Lau??aviet??":
        {
            "id": 5,
            "name": "Pentacles",
            "points": 10
        },
    "760617453167837215":
        {
            "id": 6,
            "name": "The Empress",
            "points": 10
        },
    "Titas":
        {
            "id": 7,
            "name": "The Sun",
            "points": 10
        },
    "Adomas":
        {
            "id": 8,
            "name": "The Fool",
            "points": 10
        },
    "528271831191519262":
        {
            "id": 9,
            "name": "Wheel Of Fortune",
            "points": 10
        },
    "516708046848917504":
        {
            "id": 10,
            "name": "Justice",
            "points": 10
        },
    "Med??iai":
        {
            "id": 11,
            "name": "Wands",
            "points": 10
        },
    "634406031039922197":
        {
            "id": 12,
            "name": "The Devil",
            "points": 10
        },
    "288000828684369920":
        {
            "id": 13,
            "name": "The Lovers",
            "points": 10
        },
    "346336924711124992":
        {
            "id": 14,
            "name": "The Tower",
            "points": 10
        },
    "V??liavos":
        {
            "id": 15,
            "name": "Swords",
            "points": 10
        },
    "Viktorija":
        {
            "id": 16,
            "name": "The Hierophant",
            "points": 10
        },
    "Lukas":
        {
            "id": 17,
            "name": "Temperance",
            "points": 10
        },
    "697023909337366609":
        {
            "id": 18,
            "name": "Judgement",
            "points": 10
        },
    "Ugn?? Me??kuotyt??":
        {
            "id": 19,
            "name": "The Magician",
            "points": 10
        },
    "Snacks?? zona":
        {"id": 20,
            "name": "Cups",
            "points": 10
        },
    "489412069620449280":
        {
            "id": 21,
            "name": "The Hermit",
            "points": 10
        },
    "475075704992563200":
        {
            "id": 22,
            "name": "The Moon",
            "points": 10
        },
    "256788795935031296":
        {
            "id": 23,
            "name": "The World",
            "points": 10
        },
    "689120671392989267":
        {
            "id": 24,
            "name": "Strength",
            "points": 10
        }
}