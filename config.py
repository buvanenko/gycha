import os
import dotenv

dotenv.load_dotenv()

SBER_UID = os.getenv('SBER_UID')
SBER_AUTH = os.getenv('SBER_AUTH')

VK_TOKEN = os.getenv('VK_TOKEN')

OW_TOKEN = os.getenv('OW_TOKEN')