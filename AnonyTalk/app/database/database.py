import aiomysql
import datetime
import json
import time
import hashlib


class DatabaseHandler:
    def __init__(self, host, user, passwd, databasename):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.databasename = databasename
        self.pool = None

    async def __aenter__(self):
        self.pool = await aiomysql.create_pool(host=self.host,
                                               user=self.user,
                                               password=self.passwd,
                                               db=self.databasename,
                                               autocommit=True)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.pool.close()
        await self.pool.wait_closed()

    async def execute_query(self, query, fetch_all=False):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                if fetch_all:
                    return await cursor.fetchall()
                else:
                    return await cursor.fetchone()

    async def connect_database_one(self, query):
        async with self:
            return await self.execute_query(query)

    async def connect_database_all(self, query):
        async with self:
            return await self.execute_query(query, fetch_all=True)

    async def save_data(self, query):
        async with self:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query)
                    await cursor.execute("SELECT LAST_INSERT_ID()")
                    last_insert_id = await cursor.fetchone()
                    return last_insert_id[0] if last_insert_id else None

    async def check_user(self, telegram_id: int):
        query = f"SELECT `hash_telegram_id` FROM `users` WHERE `hash_telegram_id` = '{hashlib.md5(str(telegram_id).encode('utf-8')).hexdigest()}'"
        result = await self.connect_database_one(query)
        return not bool(result)

    async def create_user(self, telegram_id: int, timestamp: int):
        await self.save_data(f"INSERT INTO `users` (`hash_telegram_id`,`timeout`) "
                             f"VALUES ('{hashlib.md5(str(telegram_id).encode('utf-8')).hexdigest()}', '{timestamp}')")
    
    async def user_gender(self, telegram_id: int):
        query = f"SELECT `gender` FROM `users` WHERE `hash_telegram_id` = '{hashlib.md5(str(telegram_id).encode('utf-8')).hexdigest()}' LIMIT 1"
        return (await self.connect_database_one(query))['gender']
    
    async def set_gender(self, telegram_id: int, gender: str):
        query = f"UPDATE `users` SET `gender` = '{gender}' WHERE `hash_telegram_id` = '{hashlib.md5(str(telegram_id).encode('utf-8')).hexdigest()}' LIMIT 1"
        await self.save_data(query)

    async def user_timeout(self, telegram_id: int):
        query = f"SELECT `timeout`,`ban` FROM `users` WHERE `hash_telegram_id` = '{hashlib.md5(str(telegram_id).encode('utf-8')).hexdigest()}' LIMIT 1"
        return await self.connect_database_one(query)

    async def set_timeout(self, telegram_id: int, timeout: int):
        await self.save_data(f"UPDATE `users` SET `timeout` = '{timeout}' WHERE `hash_telegram_id` = '{hashlib.md5(str(telegram_id).encode('utf-8')).hexdigest()}' LIMIT 1") 