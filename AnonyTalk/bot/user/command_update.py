from bot.base import *
@bot.message_handler(commands=['update'],content_types=['text'],is_ban=False,user_status=False)
async def update_message(message: telebot.types.Message):
    chat_id = message.chat.id
    await bot.send_sticker(chat_id,"CAACAgIAAxkBAAEL2zpmEN7Li-htcta5NGzcWq5Ln8EVYAACAgEAAladvQpO4myBy0Dk_zQE")
    await bot.send_message(message.chat.id,"🤖ربات شما بروز شد✅"
                           ,reply_markup=Keyboards.keyboard_user())