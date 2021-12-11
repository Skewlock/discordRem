import discord, random, logs, sqlite3, json

def valid_fun(msg):
    db = sqlite3.connect("discordRem.db")
    cursor = db.cursor()
    cursor.execute("SELECT fun FROM Servers WHERE server_id=?", (msg.guild.id,))
    valid = cursor.fetchone()
    db.close()
    if valid is None:
        return False
    return valid[0]

async def fact(msg):
    if not(valid_fun(msg)):
        logs.printWarning("Module fun not enabled.")
        return await msg.channel.send("Le module `fun` n'est pas activé, pour l'activer faites `!module enable fun`.")
    file = open("res/facts.json")
    data = json.load(file)
    number = random.randint(0, len(data))
    embed = discord.Embed(title="Fact #"+str(number + 1), description=data[number], color=0x4c99c2)
    await msg.channel.send(embed=embed)
