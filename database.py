import sqlite3, discord

async def init():
    db = sqlite3.connect("discordRem.db")
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        user_id INTEGER,
        admin BOOL,
        money INTEGER NOT NULL,
        bank_money INTEGER NOT NULL,
        PRIMARY KEY (user_id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Servers(
        server_id INTEGER,
        nsfw BOOLEAN,
        currency BOOLEAN,
        fun BOOLEAN,
        prefix VARCHAR(10),
        PRIMARY KEY (server_id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Items(
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        image TEXT
    );
    ''')
    db.commit()
    db.close()

async def init_user(msg):
    db = sqlite3.connect("discordRem.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE user_id=?", (msg.author.id,))
    values = cursor.fetchone()
    if values is None:
        cursor.execute("INSERT INTO Users VALUES ("+str(msg.author.id)+",0, 0, 0);")
        db.commit()
        await msg.channel.send("Vous avez été ajouté à la base de données.")
    else:
        await msg.channel.send("Vous êtes déjà dans la base de données.")
    db.close()


async def init_server(msg):
    db = sqlite3.connect("discordRem.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Servers WHERE server_id=?", (msg.guild.id,))
    values = cursor.fetchone()
    if values is None:
        cursor.execute("INSERT INTO Servers VALUES ("+str(msg.guild.id)+", False, False, False, \"!\");")
        db.commit()
        await msg.channel.send("Le serveur a été ajouté dans la base de données.")
    else:
        await msg.channel.send("Le serveur est déjà dans la base de données.")
    db.close()