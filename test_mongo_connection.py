from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')  # Simple test de connectivité
    print("✅ Connexion réussie à MongoDB Atlas !")
except Exception as e:
    print("❌ Erreur de connexion à MongoDB :", e)
