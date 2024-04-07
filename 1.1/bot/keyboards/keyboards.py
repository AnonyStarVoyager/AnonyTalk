from telebot import types
class Keyboards:
    staticmethod
    def keycallbackdata(text,data):
        return types.InlineKeyboardButton(text=text,callback_data=data)
    staticmethod
    def keyboard_user(type : str = "home"):
        keys = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if type == "home":
            keys.add('🎉 شروع گفتگوی هیجان‌انگیز ناشناس')
            keys.add('🛠️ مستندات فنی','📚 راهنمای استفاده')
        elif type == "back":
            keys.add('🔙 بازگشت')
        elif type == "cancel":
            keys.add('❌ لغو')
        elif type == "disconnect":
            keys.add('🔗 قطع اتصال گفتگو')
        return keys