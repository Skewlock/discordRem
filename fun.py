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
    embed.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/edb98d9c-1b66-47d8-934f-e5fe74320fbd/dc5kndw-c95fe288-4d80-4922-9357-ebd5a48ec5c0.png/v1/fill/w_751,h_1063,strp/rem_render_by_kaedetsukimiya_dc5kndw-pre.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD0xNDQ5IiwicGF0aCI6IlwvZlwvZWRiOThkOWMtMWI2Ni00N2Q4LTkzNGYtZTVmZTc0MzIwZmJkXC9kYzVrbmR3LWM5NWZlMjg4LTRkODAtNDkyMi05MzU3LWViZDVhNDhlYzVjMC5wbmciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.iRafAsDmerB9cxQYOXlGHxuOJXz1am8bYo6L7K6zefs")
    await msg.channel.send(embed=embed)
