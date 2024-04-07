from bot.base import *

@bot.message_handler(func=lambda message: True and message.text == "🛠️ مستندات فنی",user_status=False,
                     content_types=['text'],is_ban=False)
async def technical_documentation_message(message: telebot.types.Message):
    chat_id = message.chat.id
    await bot.send_sticker(chat_id,"CAACAgIAAxkBAAEL1wABZg18Agglcha726Ic_HORJQ6at4MAAk4CAAJWnb0KMP5rbYEyA280BA")
    text = """
    <b>
    🛡️ حفظ حریم خصوصی یک اصل مهم و غیرقابل چشم‌پوشی است
    🛠️ قبل از شروع به کار با ربات، لطفاً با دقت مستندات زیر را مطالعه کنید تا با خیالی آسوده از فضای مجازی لذت ببرید
    </b>
    """
    await bot.send_document(chat_id,"BQACAgQAAxkBAAM2Zg2vAAEyq8daM2-V2U9ditaKn2rqAAKLEgACE9RpULf742yAh2lUNAQ",caption=text)
    