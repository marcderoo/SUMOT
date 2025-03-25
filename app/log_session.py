from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

log_bp = Blueprint('log', __name__)

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["sumot"]
logs_collection = db["logs"]

@log_bp.route('/log-session', methods=['POST'])
def log_session():
    data = request.get_json()
    ip = request.remote_addr or request.headers.get("X-Forwarded-For", "Unknown")

    log_data = {
        "ip": ip,
        "mode": data.get("mode"),
        "victoire": data.get("victoire", False),
        "temps": data.get("temps", None),
    }

    logs_collection.insert_one(log_data)

    return jsonify({"status": "ok", "message": "Log enregistré"})
