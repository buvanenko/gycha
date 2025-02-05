
import aiohttp

import config

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload='scope=GIGACHAT_API_PERS'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': config.SBER_UID,
    'Authorization': 'Basic ' + config.SBER_AUTH
}

async def get_token():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers, ssl=False) as response:
            return await response.json()