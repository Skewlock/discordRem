import discord, requests, random, logs, sqlite3

def valid_nsfw(msg):
    db = sqlite3.connect("discordRem.db")
    cursor = db.cursor()
    cursor.execute("SELECT nsfw FROM Servers WHERE server_id=?", (msg.guild.id,))
    valid = cursor.fetchone()
    db.close()
    return valid[0]

async def rule34(msg):
    if not(valid_nsfw(msg)):
        logs.printWarning("Module nsfw not enabled.")
        return await msg.channel.send("Le module `nsfw` n'est pas activé, pour l'activer faites `!module enable nsfw`.")
    if msg.channel.is_nsfw():
        try:
            args = msg.content.split(' ')
            r = requests.get("https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1000&tags="+str(args[1])+"&json=1")
            logs.printValid(str(r.json()[random.randint(0, len(r.json()))]["file_url"])+" sent.")
            embed = discord.Embed(title="Result for "+args[1]+":", type="rich", color=0xff1c84,
            description="image not loading: [click here]("+str(r.json()[random.randint(0, len(r.json()))]["file_url"])+")")
            embed.set_image(url=str(r.json()[random.randint(0, len(r.json()))]["file_url"]))
            await msg.channel.send(embed=embed)
        except:
            logs.printWarning("No result for search "+str(args[1]))
            await msg.channel.send("Aucun résultat désolé.")
    else:
        logs.printWarning("Channel not nsfw.")
        await msg.channel.send("Vous devez être dans un channel NSFW pour faire ça.")
