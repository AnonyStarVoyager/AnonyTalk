from bot.base import *

@bot.message_handler(func=lambda message: True and (message.text == "❌ لغو" or message.text == "❌ cancel" or message.text == "🔙 بازگشت" or message.text == "🔙 back"),content_types=['text'])
async def cancel_message(message: telebot.types.Message):
    chat_id = message.chat.id
    async with lock:
        if redis_client.exists(chat_id):
            await bot.send_sticker(int(redis_client.get(chat_id)),"CAACAgIAAxkBAAEL1uxmDXtC4vogTehlyW2QnD6Mdi--dAAC8wADVp29Cmob68TH-pb-NAQ")
            await bot.send_message(int(redis_client.get(chat_id)),"✨ اوپس! به نظر می‌رسه دوست ناشناس‌ت چت رو بسته. اما نگران نباش، همیشه فرصت‌های جدیدی وجود داره! 🚀\n\n"
                                    "🌟 حالا می‌تونی با یک کلیک جادویی، یه گفتگوی تازه رو شروع کنی و به دنیای ناشناس‌ها سلام کنی! 🎈\n\n"
                                    "👇 بزن بریم، یه دوست جدید منتظره!",
                                    reply_markup=Keyboards.keyboard_user())
            if redis_client.exists(redis_client.get(chat_id)):
                redis_client.delete(redis_client.get(chat_id))
            redis_client.delete(chat_id)
        elif any(user[1] == chat_id for user in ChatConnectQueue):
            ChatConnectQueue[:] = [user for user in ChatConnectQueue if user[1] != chat_id]
        await bot.send_sticker(chat_id,"CAACAgIAAxkBAAEL1vJmDXtadmTxwEPSCU69SDS2MqqO2QACSQIAAladvQoqlwydCFMhDjQE")
        await bot.send_message(chat_id,"✨ گفتگوی تو به پایان رسید و با موفقیت بسته شد! 👏\n\n"
                            "🌈 هیچ نگرانی نیست، فرصت‌های جدیدی در انتظارند! آماده‌ای برای دوستی‌های نو؟\n\n"
                            "👇 فقط کافیه این دکمه رو فشار بدی و وارد دنیای چت‌های تازه بشی!",
                            reply_markup=Keyboards.keyboard_user())