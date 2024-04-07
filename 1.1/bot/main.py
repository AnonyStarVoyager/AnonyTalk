from bot.filter.main import *
from bot.commands.main import *
from bot.user import main
import asyncio


async def main():
    await asyncio.gather(set_bot_commands(),bot.infinity_polling(),clear_ChatConnectQueue_list(ChatConnectQueue))



asyncio.run(main())