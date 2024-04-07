from bot.base import *

@bot.message_handler(is_ban=False)
async def nothing(message: telebot.types.Message):
    pass

@bot.message_handler(is_ban=False,
                     content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact',
                                    'animation', 'dice', 'poll', 'venue', 'new_chat_members', 'left_chat_member', 'new_chat_title',
                                    'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created',
                                    'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
async def nothing(message):
    pass