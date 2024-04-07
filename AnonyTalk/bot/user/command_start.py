from bot.base import *
import re

def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None


@bot.message_handler(commands=['start'],content_types=['text'],is_ban=False)
async def strart_message(message: telebot.types.Message):
    chat_id = message.chat.id
    if await connectdatabase.check_user(chat_id):
        await connectdatabase.create_user(chat_id,int(time.time()))
        await bot.send_sticker(chat_id,"CAACAgIAAxkBAAEL121mDbSTdlYu0XT0iuDMcZhTaUz_sAACAQEAAladvQoivp8OuMLmNDQE")
        await bot.send_message(message.chat.id,"سلام ! 🌟\n\nبه <b>AnonyTalk</b> خوش اومدی، جایی که می‌تونی آزادانه و بدون دغدغه حرف دلتو بزنی. اینجا همه چی ناشناسه و فقط صدای واقعی تو شنیده می‌شه. پس با خیال راحت شروع به چت کن و لذت ببر. ما اینجاییم تا فضایی امن و صمیمی رو برات فراهم کنیم. پس بیا و بخشی از این داستان باش! 🎈✨\n\n"
                               ,reply_markup=Keyboards.keyboard_user())
    else:
        # base of data
        unique_code = extract_unique_code(message.text)
        if unique_code:
            pass
        else:
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
                    
            await bot.send_sticker(chat_id,"CAACAgIAAxkBAAEL2zhmEN0x-kMYAvXLnKI2hwMg12sfWgAC9wADVp29CgtyJB1I9A0wNAQ")
            await bot.send_message(message.chat.id,'🌌 کنجکاویت رو برانگیز و با "💬 AnonyTalk" به یک ماجراجویی ناشناس بپیوند! \n\n'
                                   '✨ دنیایی پر از امکانات ناشناس و جذاب در انتظارته. همین حالا دست به کار شو و با یک ضربه به دکمه زیر، شروع کن به پیدا کردن دوستان جدید در فضایی کاملاً ناشناس! 🎭\n\n'
                                   '👇 فقط کافیه اینجا رو لمس کنی و چت ناشناس رو شروع کنی!'
                                   '➖➖➖➖➖➖➖➖➖'
                                   ,reply_markup=Keyboards.keyboard_user())
        
    