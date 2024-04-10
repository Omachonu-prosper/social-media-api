from pymongo import MongoClient
from config import Config

client = MongoClient(Config.DB_URI)
db = client['Social_Media_API']
users = db['Users'] # Users collection