import aiosqlite
import os
import asyncio

class Database:
    def __init__(self):
        self.conn = None
        self.init_queries = [
            """
            CREATE TABLE IF NOT EXISTS temporarychannel (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER
            )
            """
        ]

    async def connect(self):
        self.conn = await aiosqlite.connect("./database/database.db")
        for query in self.init_queries:
            await self.conn.execute(query)
        await self.conn.commit()

    async def disconnect(self):
        await self.conn.close()

    # autorole
    async def get_temporarychannel(self, guild_id):
        async with self.conn.execute("SELECT * FROM temporarychannel WHERE guild_id=?", (guild_id,)) as cursor:
            row = await cursor.fetchone()

        if not row:
            return None
        else:
            return row[1]

    async def set_temporarychannel(self, guild_id, channel_id):
        await self.conn.execute("INSERT OR REPLACE INTO temporarychannel (guild_id, channel_id) VALUES (?, ?)", (guild_id, channel_id))
        await self.conn.commit()

