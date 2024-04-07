from bot.base import *

async def set_bot_commands():
    await bot.delete_my_commands(scope=telebot.types.BotCommandScopeDefault())

    await bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("start", "♻️ بزن بریم! همین الان شروع کنیم؟"),
            telebot.types.BotCommand("update", "🔄 آخرین خبرا و آپدیت‌ها رو اینجا چک کن!"),
            telebot.types.BotCommand("github", "🐙🐱 کد‌های منو اینجا ببین!"),
            telebot.types.BotCommand("donation", "💖 دوست داری حمایتم کنی؟")
        ],
        scope=telebot.types.BotCommandScopeDefault()
    )