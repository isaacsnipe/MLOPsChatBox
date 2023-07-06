import os
import motor.motor_asyncio
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://epkayang:MG8rFBeYDQJsLSaR@chatbot.8iu5fca.mongodb.net/?retryWrites=true&w=majority"

# client = MongoClient(uri)
# db = client.chatbot

client = motor.motor_asyncio.AsyncIOMotorClient(uri)

db = client.chatbot
