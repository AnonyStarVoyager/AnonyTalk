from bot.base import *
@bot.message_handler(commands=['update'],content_types=['text'],is_ban=False,user_status=False)
async def update_message(message: telebot.types.Message):
    chat_id = message.chat.id
    text = """
    📋 تغییرات بروزرسانی اخیر :
<blockquote>
🟢 یک ستون جدید به نام "timeout" به دیتابیس اضافه شد تا هم اسپم رو کنترل کنیم و هم دستمون رو برای محدودیت‌های تلگرام باز بذاریم.

🟢 جستجوی ناشناس حالا مثل برق و باده، سریع و دقیق‌تر از همیشه!

🟢  دستورات ربات به فعالیت درآمدن تا کار با من هیجان‌انگیزتر بشه.

🟢 لینک گیتهاب پروژه حالا برای دیدن همگان بازه، هر کسی می‌تونه نگاهی به کدهامون بندازه.

🟢 و خیلی تغییرات ریز دیگه که می‌تونید تو صفحه گیتهاب پروژه چشم‌تون رو روشون خوش کنید!
</blockquote>
    """
    await bot.send_sticker(chat_id,"CAACAgIAAxkBAAEL2zpmEN7Li-htcta5NGzcWq5Ln8EVYAACAgEAAladvQpO4myBy0Dk_zQE")
    await bot.send_message(message.chat.id,text,reply_markup=Keyboards.keyboard_user())