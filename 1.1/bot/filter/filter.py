from bot.base import *

class UserStep(telebot.asyncio_filters.AdvancedCustomFilter):
    key='user_step'
    @staticmethod
    async def check(message, step):
        chat_id = message.chat.id if hasattr(message, 'chat') else message.from_user.id
        return True if await connectdatabase.user_step(chat_id) == step else False


class IsBan(telebot.asyncio_filters.SimpleCustomFilter):
    key='is_ban'
    @staticmethod
    async def check(message):
        chat_id = message.chat.id if hasattr(message, 'chat') else message.from_user.id
        if await connectdatabase.check_user(chat_id):
            return False
        else:
            user_status = await connectdatabase.user_timeout(chat_id)
            ban = user_status['ban']
            if ban != 0:
                return True
            else:
                timeout = user_status['timeout']
                if timeout <= int(time.time()):
                    await connectdatabase.set_timeout(chat_id,(int(time.time())+1))
                    return False
                elif (timeout > int(time.time())) and ((timeout - int(time.time())) >= 240):
                    if (timeout - int(time.time())) >= 240:
                        await bot.send_message(chat_id,"⛔️ بخاطر اسپم کردن بن شدید"
                                            ,reply_markup=Keyboards.keyboard_user())
                        query = f"UPDATE `user` SET `step` = 'none',`ban` = '1',`timeout` = '{int(time.time())}' WHERE `Telegram_id` = '{chat_id}' LIMIT 1"
                        await connectdatabase.save_data(query)
                        return True
                    else:
                        await connectdatabase.set_timeout(chat_id,int(timeout+3))
                        return True
                else:
                    await connectdatabase.set_timeout(chat_id,(int(time.time())+3))
                    return True


class IsIntalk(telebot.asyncio_filters.SimpleCustomFilter):
    key='in_talking'
    @staticmethod
    async def check(message: telebot.types.Message):
        if redis_client.exists(message.chat.id) and redis_client.exists(redis_client.get(message.chat.id)) and int(redis_client.get(redis_client.get(message.chat.id))) == message.chat.id :
            return True
        else:
            return False

class UserStatus(telebot.asyncio_filters.SimpleCustomFilter):
    key='user_status'
    @staticmethod
    async def check(message):
        chat_id = message.chat.id if hasattr(message, 'chat') else message.from_user.id
        if redis_client.exists(chat_id):
            return True
        elif any(user[1] == chat_id for user in ChatConnectQueue):
            return True
        else:
            return False
            
bot.add_custom_filter(UserStep())
bot.add_custom_filter(IsBan())
bot.add_custom_filter(IsIntalk())
bot.add_custom_filter(UserStatus())