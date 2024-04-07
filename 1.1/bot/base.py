import telebot
from bot.keyboards import Keyboards
from app import *
from config import *
from telebot.async_telebot import AsyncTeleBot
import asyncio
import re
import math
import time
from collections import defaultdict
import redis

ChatConnectQueue = []

media_groups = defaultdict(list)

lock = asyncio.Lock()

redis_client = redis.Redis(decode_responses=True)

connectdatabase = DatabaseHandler(info_datebase['host'],info_datebase['user'],info_datebase['password'],info_datebase['database'])

bot = AsyncTeleBot(bot_token,parse_mode="HTML",allow_sending_without_reply=True,disable_web_page_preview=True,protect_content=True)

async def clear_ChatConnectQueue_list(ChatConnectQueue : list):
    while True:
        for userqueue in ChatConnectQueue:
            if userqueue[0] < (int(time.time()) - (20*60)):
                ChatConnectQueue.remove(userqueue)
            else:
                continue
        await asyncio.sleep(30*60)

            