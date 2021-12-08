import discord
import os
import commands as cmds
import logs

bot = discord.Client()
bot.prefix = "!"
print("Bot Rem 1.0:\n\n")
@bot.event
async def on_message(msg):
    # Get command
    if msg.content[0] == bot.prefix and msg.author != bot.user:
        instruction = msg.content[1:]
        command = instruction.split(" ")[0]
        logs.printInfo("Command "+command+" requested.")
        commands = {
            "hello": [cmds.hello, (msg,)],
            "ping": [cmds.ping, (msg, bot)]
        }
        # Launch command
        func = commands.get(command)
        if func is None:
            return logs.printWarning("Command "+command+" doesn't exists.\n")
        await func[0](*func[1])
        logs.printInfo("Command "+command+" successfully done.\n")

@bot.event
async def on_ready():
    logs.printValid("Bot ready !")
    logs.printValid("Default prefix: " + bot.prefix)
    logs.printValid("Mention: "+bot.user.mention+"\n")

bot.run(os.environ["TOKEN"])