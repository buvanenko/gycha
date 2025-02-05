from vkbottle.bot import Message
from vkbottle.exception_factory.base_exceptions import VKAPIError

from bot import bot


async def get(message: Message):

    try:
        members = await bot.api.messages.get_conversation_members(message.peer_id)
    except VKAPIError:
        return "Для этого я должен быть админом беседы."

    for member in members.items:
        if member.member_id == message.from_id:
            if not member.is_admin and not member.is_owner:
                return "Ты не админ, так что бана не будет."

    if "[" in message.text and "]" in message.text:
        target_id = int(message.text.split("[")[1].split("|")[0].replace("club", "-").replace("id", ""))
    elif message.reply_message is not None:
        target_id = message.reply_message.from_id
    elif len(message.fwd_messages) > 0:
        target_id = message.fwd_messages[0].from_id
    else:
        return "Не указан пользователь для бана."

    await bot.api.messages.remove_chat_user(message.chat_id, user_id=target_id)
    return "Забанил!"