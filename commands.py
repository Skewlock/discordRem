import discord, time, random, logs, sqlite3

async def help(msg):
    embed = discord.Embed(title="Menu d'aide:", color=0x24cfff)
    embed.add_field(name="📄 Commandes générales:", value="`help`, `ping`, `purge`, `profile`, `sinit`, `module`", inline=False)
    embed.add_field(name="🎉 Commandes fun:", value="`fact`", inline=False)
    embed.add_field(name="🪙 Commandes d'argent:", value="`init`, `balance`", inline=False)
    embed.add_field(name="🔞 Commandes NSFW:", value="`rule34`", inline=False)
    embed.set_image(url="https://vignette.wikia.nocookie.net/princess-connect/images/6/65/Rem-astrum-sprite-normal.png/revision/latest?cb=20190808065750")
    await msg.channel.send(embed=embed)

async def ping(msg, bot):
    time_then = time.monotonic()
    pinger = await msg.channel.send("<a:loading:743171496188575854>Calcul en cours du ping...")
    ping_ = (1000 * (time.monotonic() - time_then))
    embed = discord.Embed(name="Results :", color=0x4c99c2, type="rich")
    embed.add_field(name="Ping du bot :", value=str(int(ping_)) + "ms", inline=True)
    embed.add_field(name="Ping de l'API :", value=str(int(bot.latency * 1000)) + "ms", inline=True)
    await pinger.edit(content=":white_check_mark: Calcul terminé !", embed=embed)

async def purge(msg):
    args = msg.content.split(' ')
    if len(args) < 2:
        return await msg.channel.send("Il vous manque un argument. Vous n'avez pas spécifié le nombre de messages à suppprimer.")
    if 0 < int(args[1]) and 100 >= int(args[1]):
        await msg.channel.purge(limit=int(args[1]))
    else:
        await msg.channel.send("Le nombre de messages doit être compris entre 0 et 100.")

async def profile(msg):
    if msg.author.color == discord.Colour.default():
        color=discord.Colour.random()
    else:
        color=msg.author.color
    embed = discord.Embed(title="Profil de "+msg.author.name, color=color)
    embed.set_thumbnail(url=msg.author.avatar_url)
    embed.add_field(name=":id: User ID", value=msg.author.id, inline=False)
    embed.add_field(name=":calendar: A rejoint le serveur le", value=msg.author.joined_at, inline=False)
    await msg.channel.send(embed=embed)

async def module(msg):
    db = sqlite3.connect('discordRem.db')
    cursor = db.cursor()
    args = msg.content.split(' ')
    if len(args) < 2:
        cursor.execute("SELECT currency, nsfw, fun FROM Servers WHERE server_id=?", (msg.guild.id,))
        values = cursor.fetchone()
        if values is None:
            return await msg.channel.send("Votre serveur n'est pas dans la base de données. Pour l'y ajouter faites `!sinit`")
        embed = discord.Embed(title="Status des modules du serveur.", color=0x4c99c2)
        embed.add_field(name=":tada: Fun", value=str(bool(values[2])))
        embed.add_field(name=":underage: NSFW", value=str(bool(values[1])))
        embed.add_field(name=":coin: Currency", value=str(bool(values[0])))
        embed.set_image(url="https://3.bp.blogspot.com/-F5AU_w3sHpg/XJaN2ZFFtcI/AAAAAAAAbWo/056qtGlkeLgYlXIX2SJ5pdRl55y0E3YVQCLcBGAs/w800/05t-hXufSqtfydMWx6tKfx00Z_ZfzxstV3Qm30gZjRS0AUS-x-lkFiNYiFoKgOtc0edzIfBm76_y9uu7ozoQOtT6G6Ock2y4GN4OUNaUqFxXZg9jPrccqhII1ETEdHNhmaDeFQ2N2Ehikcm7tT7Ufg.png")
        return await msg.channel.send(embed=embed)
    try:
        if args[1] == "enable":
            if (args[2] == "currency"):
                cursor.execute("SELECT currency FROM Servers WHERE server_id=?", (msg.guild.id,))
                value = cursor.fetchone()
                if value[0] == False:
                    cursor.execute("UPDATE Servers SET currency = True WHERE server_id=?", (msg.guild.id,))
                await msg.channel.send("Le module `currency` a été activé avec succès.")
            elif (args[2] == "nsfw"):
                cursor.execute("SELECT nsfw FROM Servers WHERE server_id=?", (msg.guild.id,))
                value = cursor.fetchone()
                if value[0] == False:
                    cursor.execute("UPDATE Servers SET nsfw = True WHERE server_id=?", (msg.guild.id,))
                await msg.channel.send("Le module `nsfw` a été activé avec succès.")
            elif (args[2] == "fun"):
                cursor.execute("SELECT fun FROM Servers WHERE server_id=?", (msg.guild.id,))
                value = cursor.fetchone()
                if value[0] == False:
                    cursor.execute("UPDATE Servers SET fun = True WHERE server_id=?", (msg.guild.id,))
                await msg.channel.send("Le module `fun` a été activé avec succès.")
            else:
                await msg.channel.send("le module `"+args[2]+"` n'existe pas.")
        if args[1] == "disable":
            if (args[2] == "currency"):
                cursor.execute("SELECT currency FROM Servers WHERE server_id=?", (msg.guild.id,))
                value = cursor.fetchone()
                if value[0] == True:
                    cursor.execute("UPDATE Servers SET currency = False WHERE server_id=?", (msg.guild.id,))
                await msg.channel.send("Le module `currency` a été désactivé avec succès.")
            elif (args[2] == "nsfw"):
                cursor.execute("SELECT nsfw FROM Servers WHERE server_id=?", (msg.guild.id,))
                value = cursor.fetchone()
                if value[0] == True:
                    cursor.execute("UPDATE Servers SET nsfw = False WHERE server_id=?", (msg.guild.id,))
                await msg.channel.send("Le module `nsfw` a été désactivé avec succès.")
            elif (args[2] == "fun"):
                cursor.execute("SELECT fun FROM Servers WHERE server_id=?", (msg.guild.id,))
                value = cursor.fetchone()
                if value[0] == True:
                    cursor.execute("UPDATE Servers SET fun = False WHERE server_id=?", (msg.guild.id,))
                await msg.channel.send("Le module `fun` a été désactivé avec succès.")
            else:
                await msg.channel.send("le module `"+args[2]+"` n'existe pas.")
    except IndexError:
        await msg.channel.send("Il vous manque un argument.")
    db.commit()
    db.close()