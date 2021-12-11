import discord, os, logs
import commands as cmds
import database as db
import nsfw
import currency as curr
import fun

bot = discord.Client()
bot.prefix = "!"

print("Bot Rem 1.0:\n\n")
@bot.event
async def on_message(msg):
    # Get command
    if msg.author != bot.user:
        if msg.content[0] == bot.prefix:
            instruction = msg.content[1:]
            command = instruction.split(" ")[0]
            logs.printInfo("Command "+command+" requested.")
            commands = {
                #General commands
                "ping": [cmds.ping, (msg, bot)],
                "purge": [cmds.purge, (msg,)],
                "help": [cmds.help, (msg,)],
                "sinit": [db.init_server, (msg,)],
                "module": [cmds.module, (msg,)],

                #Fun commands
                "fact": [fun.fact, (msg,)],

                #Currency commands
                "init": [db.init_user, (msg,)],
                "profile": [cmds.profile, (msg,)],
                "balance": [curr.balance, (msg,)],

                #NSFW commands
                "rule34": [nsfw.rule34, (msg,)],
                #"porn": [cmds.porn, (msg,)]
            }
            # Launch command
            func = commands.get(command)
            if func is None:
                return logs.printWarning("Command "+command+" doesn't exists.\n")
            await func[0](*func[1])
            logs.printInfo("Command "+command+" successfully done.\n")

@bot.event
async def on_ready():
    await db.init()
    logs.printValid("Bot ready !")
    logs.printValid("Default prefix: " + bot.prefix)
    logs.printValid("Mention: "+bot.user.mention+"\n")
    await bot.change_presence(activity=discord.Streaming(name="Prefix: !",
    plateform="Twitch", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", game="test"))


bot.run(os.environ["TOKEN"])