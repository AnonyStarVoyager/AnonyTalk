from bot.base import *


@bot.message_handler(func=lambda message: True and message.text == "🎉 شروع گفتگوی هیجان‌انگیز ناشناس",user_status=False,
                     content_types=['text'],is_ban=False)
async def new_anonytalk_message(message: telebot.types.Message):
    chat_id = message.chat.id
    user_gender = await connectdatabase.user_gender(chat_id)
    if user_gender == None:
        set_gender = telebot.types.InlineKeyboardMarkup()
        set_gender.add(Keyboards.keycallbackdata("👨‍🎓 پسرم","isGender_M"),Keyboards.keycallbackdata("👩‍🎓 دخترم","isGender_W"))
        await bot.send_message(chat_id,"🌈 هویتت چیزیه که تو رو منحصر به فرد می‌کنه! برای اینکه بتونیم بهترین تجربه چت رو برات فراهم کنیم، لطفاً جنسیتت رو به ما بگو\n\n"
                               "⚠️ یه لحظه وایسا و با دقت انتخاب کن چون بعد از ثبت، دیگه نمی‌تونی تغییرش بدی",
                               reply_markup=set_gender)
    else:
        find_gender = telebot.types.InlineKeyboardMarkup()
        find_gender.add(Keyboards.keycallbackdata("👱‍♂️ با یک پسر","fiGender_M"),Keyboards.keycallbackdata("👱‍♀️ با یک دختر","fiGender_W"))
        find_gender.add(Keyboards.keycallbackdata("👱 فرقی نداره","fiGender_MW"))
        await bot.send_message(chat_id,"🌟 حالا وقت انتخابه! دوست داری با کی یه چت دوستانه داشته باشی؟\n\n"
                               "⚠️ فقط یه یادآوری دوستانه: گاهی اوقات ممکنه جنسیتی که نشون داده می‌شه دقیق نباشه، پس با همون روحیه خوب همیشگیت آماده باش!\n\n"
                               "👇 انتخابت رو بکن و تا بریم سراغ یه چت جدید!",
                               reply_markup=find_gender)
        
@bot.callback_query_handler(func=lambda call: True and call.data.startswith("isGender_"),is_ban=False)
async def set_gender_query(call : telebot.types.CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    user_gender = await connectdatabase.user_gender(chat_id)
    
    if user_gender == None:
        gender = call.data.split("_")[1]
        await connectdatabase.set_gender(chat_id,gender)
    else:
        await bot.answer_callback_query(call.id,"📛 شما قبلا جنسیت خود را ثبت کرده‌اید",True)

    find_gender = telebot.types.InlineKeyboardMarkup()
    find_gender.add(Keyboards.keycallbackdata("👱‍♂️ با یک پسر","fiGender_M"),Keyboards.keycallbackdata("👱‍♀️ با یک دختر","fiGender_W"))
    find_gender.add(Keyboards.keycallbackdata("👱 فرقی نداره","fiGender_MW"))
    await bot.edit_message_text("🌟 حالا وقت انتخابه! دوست داری با کی یه چت دوستانه داشته باشی؟\n\n"
                               "⚠️ فقط یه یادآوری دوستانه: گاهی اوقات ممکنه جنسیتی که نشون داده می‌شه دقیق نباشه، پس با همون روحیه خوب همیشگیت آماده باش!\n\n"
                               "👇 انتخابت رو بکن و تا بریم سراغ یه چت جدید!",
                                chat_id,message_id,reply_markup=find_gender)
    
@bot.callback_query_handler(func=lambda call: True and call.data.startswith("fiGender_"),is_ban=False)
async def set_gender_query(call : telebot.types.CallbackQuery):
    chat_id = call.message.chat.id
    async with lock:
        if not redis_client.exists(chat_id):
            message_id = call.message.id
            await bot.delete_message(chat_id,message_id)
            user_gender = await connectdatabase.user_gender(chat_id)
            f_gender = str(call.data.split("_")[1])
            while True:
                async with lock:
                    status_find = ConversationDirector.connection(ChatConnectQueue,[int(time.time()),chat_id,user_gender,f_gender])
                if status_find['status'] == "create":
                    await bot.send_message(chat_id,"🔎 صبر کن، داریم برات یه هم‌صحبت جذاب پیدا می‌کنیم...\n\n"
                                        "🌟 اگه تا 20 دقیقه دیگه همراهت رو نیافتیم، ناامید نشو! یه شانس دیگه به سرنوشت بده و دوباره امتحان کن",
                                        reply_markup=Keyboards.keyboard_user("disconnect"))
                    break
                elif status_find['status'] == "finded":
                    redis_client.mset({status_find['users'][0] : status_find['users'][1],
                                       status_find['users'][1] : status_find['users'][0]})
                    try:
                        for userinchat in status_find['users']:
                            await bot.send_sticker(userinchat,"CAACAgIAAxkBAAEL1wRmDXxEqlezMz3Rt5y_AaL9d0wKKAACSgIAAladvQrJasZoYBh68DQE")
                            await bot.send_message(userinchat,"🌟 وای! به تازگی یک دوست ناشناس برای تو پیدا کردم که مشتاق شنیدن صدای توست\n\n"
                                                "🗨️ حالا وقتشه که شیرینی صحبت‌ها رو باهاش تجربه کنی. پس بزن بریم و چت رو شروع کن! 🚀",
                                                reply_markup=Keyboards.keyboard_user("disconnect"))
                        break
                    except:
                        continue
        else:
            await bot.answer_callback_query(call.id,"✨ هیجان در جریانه! شما الان در دنیای چت ناشناس غرق شدی. 🌀\n\n"
                                            "🚫 قبل از شیرجه زدن به گفتگوی بعدی، بیا و چت فعلیت رو با یک خداحافظی شیک به پایان ببر. بعدش می‌تونی با کلی آمادگی به سمت ماجراجویی بعدیت بری! 🌟\n\n"
                                            "👉 پس یه نفس عمیق بکش و با اتمام این چت، آماده شو برای دوستی‌های تازه!",True)
        
@bot.message_handler(func=lambda message: message.text == "🔗 قطع اتصال گفتگو", content_types=['text'])
async def cancel_key(message: telebot.types.Message):
    chat_id = message.chat.id
    if redis_client.exists(chat_id) or any(user[1] == chat_id for user in ChatConnectQueue):
        key_cancel = telebot.types.InlineKeyboardMarkup(row_width=1)
        yes_button = Keyboards.keycallbackdata("⛓️‍💥 بله، بی‌خیالش شو", "disconnect_1")
        no_button = Keyboards.keycallbackdata("‼️ نه، هنوز حرف دارم", "disconnect_0")
        key_cancel.add(yes_button, no_button)
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=message.message_id,
            text="🌪️ وایسا! داری چت رو قطع می‌کنی؟ اگه دلت گرفته و می‌خوای بری، کافیه روی 'بله، بی‌خیالش شو' بزنی. ولی اگه می‌خوای چتت رو ادامه بدی و شاید یه دوست خفن پیدا کنی، 'نه، هنوز حرف دارم' رو بزن. حالا خود دانی، رفیق!",
            reply_markup=key_cancel
        )
    else:
        await bot.send_sticker(chat_id,"CAACAgIAAxkBAAEL2zhmEN0x-kMYAvXLnKI2hwMg12sfWgAC9wADVp29CgtyJB1I9A0wNAQ")
        await bot.send_message(message.chat.id,'🌌 کنجکاویت رو برانگیز و با "💬 AnonyTalk" به یک ماجراجویی ناشناس بپیوند! \n\n'
                                '✨ دنیایی پر از امکانات ناشناس و جذاب در انتظارته. همین حالا دست به کار شو و با یک ضربه به دکمه زیر، شروع کن به پیدا کردن دوستان جدید در فضایی کاملاً ناشناس! 🎭\n\n'
                                '👇 فقط کافیه اینجا رو لمس کنی و چت ناشناس رو شروع کنی!'
                                '➖➖➖➖➖➖➖➖➖'
                                ,reply_markup=Keyboards.keyboard_user())

@bot.callback_query_handler(func=lambda call: True and call.data.startswith("disconnect_"),is_ban=False)
async def canel_conversiton(call : telebot.types.CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    choice = int(call.data.split("_")[1])
    await bot.delete_message(chat_id,message_id)
    if choice == 1:
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

# Message handler for media group messages
@bot.message_handler(func=lambda message: message.media_group_id is not None,in_talking=True,content_types=['photo', 'video', 'document'])
async def handle_media_group_message(message: telebot.types.Message):
    chat_id = message.chat.id
    media_group_id = message.media_group_id
    
    file_id = None
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
    elif message.content_type == 'video':
        file_id = message.video.file_id
    elif message.content_type == 'document':
        file_id = message.document.file_id
    
    # Add the media to the media group
    if file_id:
        media_groups[media_group_id].append(telebot.types.InputMedia(type=message.content_type, media=file_id,caption=message.caption))

    await asyncio.sleep(1.2)
    async with lock:
        if media_group_id in media_groups:
            try:
                
                await bot.send_media_group(int(redis_client.get(chat_id)), media_groups[media_group_id])
                
                del media_groups[media_group_id]
            except:
                if redis_client.exists(chat_id):
                    if redis_client.exists(redis_client.get(chat_id)):
                        redis_client.delete(redis_client.get(chat_id))
                    redis_client.delete(chat_id)
                await bot.send_sticker(chat_id,"CAACAgIAAxkBAAEL1uxmDXtC4vogTehlyW2QnD6Mdi--dAAC8wADVp29Cmob68TH-pb-NAQ")
                await bot.send_message(chat_id,"✨ اوپس! به نظر می‌رسه دوست ناشناس‌ت چت رو بسته. اما نگران نباش، همیشه فرصت‌های جدیدی وجود داره! 🚀\n\n"
                                    "🌟 حالا می‌تونی با یک کلیک جادویی، یه گفتگوی تازه رو شروع کنی و به دنیای ناشناس‌ها سلام کنی! 🎈\n\n"
                                    "👇 بزن بریم، یه دوست جدید منتظره!",
                                    reply_markup=Keyboards.keyboard_user())
            await asyncio.sleep(0.41)





@bot.message_handler(in_talking=True,
                     content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text',
                                    'venue', 'video', 'video_note', 'voice'])
async def intalking_message(message : telebot.types.Message):
    chat_id = message.chat.id
    message_id = message.id
    async with lock:
        try:
            await bot.copy_message(int(redis_client.get(chat_id)),chat_id,message_id)
        
        except:
            if redis_client.exists(chat_id):
                if redis_client.exists(redis_client.get(chat_id)):
                    redis_client.delete(redis_client.get(chat_id))
                redis_client.delete(chat_id)
                await bot.send_sticker(chat_id,"CAACAgIAAxkBAAEL1uxmDXtC4vogTehlyW2QnD6Mdi--dAAC8wADVp29Cmob68TH-pb-NAQ")
                await bot.send_message(chat_id,"✨ اوپس! به نظر می‌رسه دوست ناشناس‌ت چت رو بسته. اما نگران نباش، همیشه فرصت‌های جدیدی وجود داره! 🚀\n\n"
                                    "🌟 حالا می‌تونی با یک کلیک جادویی، یه گفتگوی تازه رو شروع کنی و به دنیای ناشناس‌ها سلام کنی! 🎈\n\n"
                                    "👇 بزن بریم، یه دوست جدید منتظره!",
                                    reply_markup=Keyboards.keyboard_user())
        await asyncio.sleep(0.41)

