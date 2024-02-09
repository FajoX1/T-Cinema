import aiosqlite

async def get_all():
    async with aiosqlite.connect("./tcinema.db") as connection:
        async with connection.execute("SELECT * FROM films") as cursor:
            result = await cursor.fetchall()
    return result
