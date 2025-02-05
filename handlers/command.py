
from vkbottle.bot import Message

from handlers import weather, ban

async def get(message: Message, command: str):
    if "WEATHER" in command:
        if "CITY" in command:
            city = command.split("CITY: ")[1]
        else:
            city = "Krasnodar"
        return await weather.get(city)

    elif "BAN" in command:
        return await ban.get(message)