"""Test de connexion à la base MongoDB via URI dans le fichier .env."""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')  # Simple test de connectivité
    print("✅ Connexion réussie à MongoDB Atlas !")
except PyMongoError as e:
    print("❌ Erreur de connexion à MongoDB :", e)
