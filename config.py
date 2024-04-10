import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_ENV = os.getenv('APP_ENVIRONMENT')
    API_KEY = os.getenv('API_KEY')
    DB_URI = os.getenv('DB_URI')