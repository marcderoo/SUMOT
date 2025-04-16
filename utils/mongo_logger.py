"""Module de log MongoDB pour l'application SUMOT."""

import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Connexion Mongo (utilise ton URI stockée dans une variable d'env)
uri = os.getenv("MONGO_URI")  # ex: "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sumot"]
collection = db["logs"]

def log_game(ip_address, mode, victory):
    """Enregistre une session de jeu dans MongoDB."""
    doc = {
        "ip": ip_address,
        "mode": mode,
        "victory": victory,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(doc)
