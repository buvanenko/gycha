
from handlers import weather

async def get(command: str):
    if "WEATHER" in command:
        if "CITY" in command:
            city = command.split("CITY: ")[1]
        else:
            city = "Krasnodar"
        return await weather.get(city)
    elif "BAN" in command:
        return "Пока не умею банить, фича в разработке."