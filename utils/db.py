from pymongo import MongoClient
from config import Config

client = MongoClient(Config.DB_URI)
db = client['Social_Media_API']
users = db['Users'] # Users collection
posts = db['Posts'] # Posts collection
notifications = db['Notifications'] # Notifications collection