import os

from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_name = os.getenv('SESSION_NAME')

if not all([api_id, api_hash, session_name]):
    raise ValueError('Необходимо указать API_ID, API_HASH и SESSION_NAME в файле .env')
