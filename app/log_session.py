from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["sumot"]              # Nom de ta base
collection = db["logs"]          # Nom de ta collection

log_bp = Blueprint('log_session', __name__)

@log_bp.route('/log-session', methods=['POST'])
def log_session():
    try:
        data = request.get_json()

        log = {
            "ip": request.remote_addr,
            "mode": data.get("mode"),
            "victoire": data.get("victoire"),
            "temps": data.get("temps"),
            "timestamp": datetime.utcnow()
        }

        collection.insert_one(log)

        return jsonify({"status": "success", "log": log}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
