import config
from vkbottle.bot import Bot, Message

import sber
import handlers

bot = Bot(token=config.VK_TOKEN)

@bot.on.message(text="пинг")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(user_ids=[message.from_id])
    print(users_info)
    await message.answer("ПОНГ")

@bot.on.message()
async def chitchat(message: Message):
    await bot.api.messages.set_activity(peer_id=message.peer_id, type="typing")
    if "[club229271933|@gycha_bot]" in message.text:
        message.text = message.text.replace("[club229271933|@gycha_bot]", "ГычаБот")
    answer = await sber.chat.get_response(message.text, message.peer_id)
    if "COMMAND: " in answer:
        answer = await handlers.command.get(answer.split("COMMAND: ")[1])
        sber.chat.add_message(message.peer_id, "assistant", answer)

    await message.answer(answer)

bot.run_forever()
