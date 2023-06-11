import asyncpg, os
from dotenv import load_dotenv

load_dotenv()

class SupabaseDatabase:
    def __init__(self):
        self.host = os.getenv("POSTGRESQL_HOST")
        self.port = os.getenv("POSTGRESQL_PORT")
        self.database = os.getenv("POSTGRESQL_DATABASE")
        self.user = os.getenv("POSTGRESQL_USER")
        self.password = os.getenv("POSTGRESQL_PASSWORD")
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )

    async def disconnect(self):
        await self.pool.close()

    #temporary_channel
    async def get_temporary_channel_id(self, guild_id):
        async with self.pool.acquire() as connection:
            result = await connection.fetch(f"SELECT temporary_channel_id FROM guilds WHERE guild_id={guild_id}")
            return result[0]['temporary_channel_id']

    async def set_temporary_channel_id(self, guild_id, channel_id):
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO guilds (guild_id, temporary_channel_id) VALUES ({guild_id}, {channel_id}) ON CONFLICT (guild_id) DO UPDATE SET temporary_channel_id={channel_id}")

    #automatic_role
    async def get_automatic_role_id(self, guild_id):
        async with self.pool.acquire() as connection:
            result = await connection.fetch(f"SELECT * FROM guilds WHERE guild_id={guild_id}")
            return result

    #human
    async def set_automatic_human_role_id(self, guild_id, role_id):
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO guilds (guild_id, human_role_id) VALUES ({guild_id}, {role_id}) ON CONFLICT (guild_id) DO UPDATE SET human_role_id={role_id}")

    #bot
    async def set_automatic_bot_role_id(self, guild_id, role_id):
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO guilds (guild_id, bot_role_id) VALUES ({guild_id}, {role_id}) ON CONFLICT (guild_id) DO UPDATE SET bot_role_id={role_id}")
