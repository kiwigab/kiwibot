import asyncpg, os, json
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


    async def delete_guild_data(self, guild_id):
        async with self.pool.acquire() as connection:
            result = await connection.fetch(f"SELECT * FROM guilds WHERE guild_id={guild_id}")

            if result:
                await connection.execute(f"DELETE FROM guilds WHERE guild_id={guild_id}")

    #temporary_channel
    async def get_guild_data(self, guild_id):
        async with self.pool.acquire() as connection:
            result = await connection.fetch(f"SELECT * FROM guilds WHERE guild_id={guild_id}")
            return result

    async def set_temporary_channel_id(self, guild_id, channel_id):
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO guilds (guild_id, temporary_channel_id) VALUES ({guild_id}, {channel_id}) ON CONFLICT (guild_id) DO UPDATE SET temporary_channel_id={channel_id}")

    #automatic roles
    async def set_automatic_human_role_id(self, guild_id, role_id):
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO guilds (guild_id, human_role_id) VALUES ({guild_id}, {role_id}) ON CONFLICT (guild_id) DO UPDATE SET human_role_id={role_id}")

    async def set_automatic_bot_role_id(self, guild_id, role_id):
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO guilds (guild_id, bot_role_id) VALUES ({guild_id}, {role_id}) ON CONFLICT (guild_id) DO UPDATE SET bot_role_id={role_id}")

    #messages
    async def set_welcome(self, guild_id, json_obj):
        async with self.pool.acquire() as connection:
            json_str = json.dumps(json_obj) 
            await connection.execute(
                "INSERT INTO guilds (guild_id, welcome) VALUES ($1, $2::jsonb) "
                "ON CONFLICT (guild_id) DO UPDATE SET welcome = $2::jsonb",
                guild_id,
                json_str
            )

    async def set_goodbye(self, guild_id, json_obj):
        async with self.pool.acquire() as connection:
            json_str = json.dumps(json_obj) 
            await connection.execute(
                "INSERT INTO guilds (guild_id, goodbye) VALUES ($1, $2::jsonb) "
                "ON CONFLICT (guild_id) DO UPDATE SET goodbye = $2::jsonb",
                guild_id,
                json_str
            )