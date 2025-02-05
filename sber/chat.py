import sber.auth as auth
import time

import aiohttp

access_token = {'access_token': "", 'expires_at': 0}
async def get_token():
    global access_token
    if time.time() > access_token['expires_at']:
        access_token = await auth.get_token()
    return access_token['access_token']

context = {}
def get_messages(chat_id: int):
    global context
    try:
        if len(context[chat_id]) > 15:
            context[chat_id] = context[chat_id][-15:]
        return context[chat_id]
    except KeyError:
        return []

def add_message(chat_id: int, role: str, content: str):
    global context
    message = {"created_at":int(time.time()),"role":role,"content":content}
    try:
        context[chat_id].append(message)
    except KeyError:
        context[chat_id] = [message]


async def prepare_payload(message: str, chat_id: int):
    tk = await get_token()
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {tk}'
    }
    messages = get_messages(chat_id)
    payload={
        "model": "GigaChat",
        "messages": [{"role":"system","content":"Тебя зовут ГычаБот. Ты чат-бот ВКонтакте мужского пола, созданный для\
         администрирования бесед. Если тебя просят забанить/заблокировать пользователя, ты отвечаешь \"COMMAND: BAN\" \
         без уточняющих вопросов. Если тебя cпросят погоде, ты отвечаешь \"COMMAND: WEATHER\" или \"COMMAND: WEATHER, CITY: Город из сообщения на английском\".\
         В остальных случаях веди непринуждённую беседу. Общайся только на \"ты\"."}] + messages,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    }
    return headers, payload


async def get_response(message: str, chat_id: int):

    add_message(chat_id, "user", message)

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers, payload = await prepare_payload(message, chat_id)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()

    answer = data['choices'][0]['message']['content']
    add_message(chat_id, "assistant", answer)

    return answer

async def weather(data):
    tk = await get_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {tk}'
    }
    message = {"created_at":1738750314,"role":"user","content":"Преобразуй данные в описание погоды. \
    Не используй форматирование текста, не передавай техническую информацию. Пиши только на русском языке. Данные: " + str(data)}
    payload={
        "model": "GigaChat",
        "messages": [message],
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()

    return data['choices'][0]['message']['content']