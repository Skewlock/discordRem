import discord, sqlite3, logs

def valid_currency(msg):
    db = sqlite3.connect("discordRem.db")
    cursor = db.cursor()
    cursor.execute("SELECT currency FROM Servers WHERE server_id=?", (msg.guild.id,))
    valid = cursor.fetchone()
    db.close()
    if valid is None:
        return False
    return valid[0]

async def balance(msg):
    if not(valid_currency(msg)):
        logs.printWarning("Module currency enabled.")
        return await msg.channel.send("Le module `currency` n'est pas activé, pour l'activer faites `!module enable currency`.")
    db = sqlite3.connect("discordRem.db")
    cursor = db.cursor()
    cursor.execute("SELECT money, bank_money FROM Users WHERE user_id=?", (msg.author.id,))
    value = cursor.fetchone()
    if value is None:
        await msg.channel.send("Vous n'êtes pas dans la base de donnée, pour y être faites `!init`.")
    else:
        embed = discord.Embed(title="Votre argent:", color=0xe6ca03)
        embed.add_field(name=":coin: Argent sur vous:", value=str(value[0]), inline=True)
        embed.add_field(name=":bank: Argent en banque:", value=str(value[1]), inline=True)
        await msg.channel.send(embed=embed)
    db.close()