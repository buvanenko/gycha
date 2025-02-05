from vkbottle.bot import Message

from bot import bot

import sber
import handlers


@bot.on.message(text="пинг")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(user_ids=[message.from_id])
    print(users_info)
    print(message)
    await message.answer("ПОНГ")

@bot.on.message()
async def chitchat(message: Message):
    ignore = True
    if message.peer_id != message.from_id:
        if "[club229271933|@gycha_bot]" in message.text:
            ignore = False
        elif message.reply_message is not None and message.reply_message.from_id == -229271933:
            ignore = False
        elif len(message.fwd_messages) > 0 and message.fwd_messages[0].from_id == -229271933:
            ignore = False

    if ignore:
        return

    await bot.api.messages.set_activity(peer_id=message.peer_id, type="typing")
    if "[club229271933|@gycha_bot]" in message.text:
        message.text = message.text.replace("[club229271933|@gycha_bot]", "ГычаБот")
    answer = await sber.chat.get_response(message.text, message.peer_id)
    if "COMMAND: " in answer:
        command = answer.split("COMMAND: ")[1]
        answer = await handlers.command.get(message, command)
        sber.chat.add_message(message.peer_id, "assistant", answer)

    await message.answer(answer, reply_to=message.id)

bot.run_forever()
