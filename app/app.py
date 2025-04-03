from typing import List, Dict, Optional, Union
from flask import Flask, render_template, send_file, request, jsonify
import random
import requests
from bs4 import BeautifulSoup
from functools import lru_cache
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, timezone
import os
import json
import boto3
from pymongo import MongoClient
from dotenv import load_dotenv
from dateutil import parser
from unidecode import unidecode

def read_file_from_s3(key):
    """Lit un fichier depuis S3 et retourne son contenu"""
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier S3 {key}: {e}")
        # Fallback vers le fichier local
        try:
            with open(key.split('/')[-1], 'r') as file:
                return file.read()
        except Exception as local_e:
            print(f"Erreur lors de la lecture du fichier local {key.split('/')[-1]}: {local_e}")
            return None

def get_path(full_path: str) -> str:
    """
    Get the full path of a file in the project.
    """
    root = os.path.dirname(os.path.abspath(__file__))

    # Go up until we find the LICENSE file
    while not os.path.exists(os.path.join(root, "LICENSE")):
        new_root = os.path.dirname(root)
        if new_root == root:  # Évite une boucle infinie
            raise FileNotFoundError("LICENSE file not found")
        root = new_root
    if "\\" in root :
        full_path = full_path.replace("/", "\\")
    else:
        full_path = full_path.replace("\\", "/")
    return str(os.path.join(root, full_path))

# Configuration du client S3
s3 = boto3.client(
    "s3",
    endpoint_url = 'https://minio.lab.sspcloud.fr',
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token = os.getenv("AWS_SESSION_TOKEN")
)


bucket_name = 'lvong'

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["sumot"]
logs_collection = db["logs"]

daily_word = "DEFAUT"

app = Flask(__name__)

os.chdir(os.path.dirname(__file__))

# Chargement du dictionnaire depuis S3
dico_content = read_file_from_s3('sumot/small_dico.txt')
if dico_content:
    dico = [line.strip() for line in dico_content.splitlines()]
else:
    # Fallback
    with open("small_dico.txt", 'r') as file:
        dico = [line.strip() for line in file]

# Chargement des fréquences de lettres depuis S3
freq_content = read_file_from_s3('sumot/frequences_lettres.txt')
if freq_content:
    frequences_lettres = {}
    for ligne in freq_content.splitlines():
        if " : " in ligne:
            lettre, freq = ligne.split(" : ")
            frequences_lettres[lettre.strip()] = float(freq.strip())
else:
    # Fallback
    with open("frequences_lettres.txt", "r") as file:
        frequences_lettres = {
            ligne.split(" : ")[0].strip(): float(ligne.split(" : ")[1].strip())
            for ligne in file if " : " in ligne
        }

def get_daily_word():
    global daily_word
    try:
        url = "https://api.magicapi.dev/api/v1/datarise/twitter/trends/?woeid=23424819"
        response = requests.get(url, headers={
            "accept": "application/json",
            "x-magicapi-key": os.getenv("X-MAGICAPI-KEY")
        },
        timeout=5)
        response.raise_for_status()
        response_json = response.json()

        trends = [trend["name"] for trend in response_json[0]['trends'] if trend["tweet_volume"] is not None]
        
        for trend in trends:
            words = unidecode(trend).lower().split(" ")
            for word in words:
                if word in dico:
                    daily_word = word.upper()
                    return

    except Exception as e:
        print(f"Erreur lors de la récupération des tendances : {e}")
    
    daily_word = random.choice(dico).upper()

@app.route('/', methods=['POST', 'GET']) 
def menu()-> str:
    return render_template('menu.html')

@app.route('/solo', methods=['POST', 'GET'])
def solo()-> str:
    score: int = 0
    count: int = 1
    
    if request.method == 'POST':
        score: int = request.form.get('score', 0, type=int)  # Score retrieval from form
        count: int = request.form.get('count', 1, type=int)  # Word count retrival from form

    random_word = random.choice(dico).upper()  # Real word
    return render_template('solo.html', data={
        "word": random_word,
        "score": score,
        "count": count
    })

@app.route('/versus_ia', methods=['POST', 'GET'])
def versus_ia()-> str:
    score: int = 0
    count: int = 1
    
    if request.method == 'POST':
        score = request.form.get('score', 0, type=int)  # Score retrieval from form
        count = request.form.get('count', 1, type=int)  # Word count retrival from form

    random_word = random.choice(dico).upper()  # Real word
    return render_template('versusia.html', data={
        "word": random_word,
        "score": score,
        "count": count
    })

@app.route('/daily', methods=['POST', 'GET'])
def daily()-> str:
    global daily_word
    return render_template('daily.html', data={
        "word": daily_word,
        "score": 0,
        "count": 1
    })

@app.route('/regles')
def regles()-> str:
    return render_template('regles.html')

@app.route('/robots.txt')
def robots()-> str:
    return send_file('static/robots.txt')

@app.route('/dico/<filename>')
def get_dico(filename: str)-> Union[str, bytes]:
    # Essayer de récupérer le fichier depuis S3
    try:
        content = read_file_from_s3(f'sumot/dico/{filename}')
        if content:
            # Créer un fichier temporaire pour le renvoyer
            temp_path = os.path.join('/tmp', filename)
            with open(temp_path, 'w') as f:
                f.write(content)
            return send_file(temp_path)
    except Exception as e:
        print(f"Erreur lors de la récupération du fichier depuis S3: {e}")
    
    # Fallback vers le fichier local
    return send_file('dico/' + filename)

@app.route('/def/<mot>')
def get_def(mot: str) -> str:
    def definition_larousse(mot: str) -> str:
        url = f"https://www.larousse.fr/dictionnaires/francais/{mot}"
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            definition = soup.find("ul", class_="Definitions")
            if definition:
                premier_element = definition.find("li")
                if premier_element:
                    return premier_element.text.strip()
            return "err"
        except Exception:
            return "err"

    def definition_wiktionnaire(mot: str) -> str:
        url = f"https://fr.wiktionary.org/wiki/{mot}"
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            definition = soup.find("ol")
            if definition:
                premier_element = definition.find("li")
                if premier_element:
                    return premier_element.text.split("\n")[0].strip()
            return "err"
        except Exception:
            return "err"

    definition = definition_larousse(mot)
    if definition != "err":
        return "0" +  definition
    
    definition = definition_wiktionnaire(mot)
    if definition != "err":
        return "1" + definition

    return "err"
    
@lru_cache(maxsize=None)
def somme_frequences(mot: str) -> float:
    return sum(frequences_lettres.get(lettre, 0) for lettre in mot)

@app.route('/ia/<difficulte>', methods=['POST'])
def bot_proposition_difficile(difficulte: str) -> Optional[str]:
    """
        Le bot utilise toutes les couleurs pour filtrer les mots possibles, sans gestion de lettres consommées.
        data["len"] : longueur du mot
        data["firstLetter"] : première lettre du mot (en majuscule)
        data["stateLetters"] : contient un résumé des informations obtenues sur chaque lettre, par exemple:
            stateLetters = {
                "A" : {
                    count : 2,
                    posValid : [0, 2],
                    posGood : [3, 4],
                    notMore : true
                }
            }
        data["validLetters"] : contient les lettres valides et leur position
        data["history"] : contient les derniers mots testés
    """
    difficulte: int = int(difficulte)
    data: Dict[str, Union[int, List[str], Dict[str, Dict[str, Union[int, bool, List[int]]]]]] = request.get_json()
    words: List[str] = [word.upper() for word in dico if len(word) == data["len"] and word[0].upper() == data["firstLetter"] and word not in data["history"]]

    filtred: List[str] = []
    for word in words:
        if difficulte > 0:
            countLetters: Dict[str, int] = {}
            goToNext = False
            for letter in word:
                if letter in countLetters:
                    countLetters[letter] += 1
                else:
                    countLetters[letter] = 1
                if difficulte > 1 and letter in data["stateLetters"] and countLetters[letter] > data["stateLetters"][letter]["count"] and data["stateLetters"][letter]["notMore"]:
                    goToNext = True
                    break
            if goToNext:
                continue

            for letter in data["stateLetters"].keys():
                if (letter not in countLetters and data["stateLetters"][letter]["count"] > 0) or (letter in countLetters and data["stateLetters"][letter]["count"] > countLetters[letter]):
                    goToNext = True
            if goToNext:
                continue

        for i in range(data["len"]):
            if difficulte > 0 and word[i] in data["stateLetters"] and i in data["stateLetters"][word[i]]["posGood"]:
                break

            if data["validLetters"][i]:
                if word[i] != data["validLetters"][i]:
                    break

            if i == data["len"] - 1:
                filtred.append(word)

    if difficulte == 3:
        mots_uniques: List[str] = [mot for mot in filtred if len(set(mot)) == len(mot)]
        filtred = max(mots_uniques or filtred , key=somme_frequences)
    else:
        filtred = random.choice(filtred)

    return filtred

@app.route('/dashboard')
def dashboard()-> str:
    return render_template('dashboard.html')

@app.route('/table')
def table()-> str:
    title = request.args.get('title', 'Sans titre')

    params = request.args.to_dict()
    params.pop('title', None)  # Supprimer le paramètre 'title' de la liste des paramètres

    # Essayer de récupérer le fichier JSON depuis S3
    with app.test_client() as client:
        response = client.get('/fetch', query_string=params)
        if response.status_code == 200:
            data = response.get_json()
        else:
            # Fallback vers une liste vide si la récupération échoue
            data = []

    return render_template('table.html', data={
        "title" : title,
        "content" : json.dumps(data)
    })

@app.route('/fetch')
def fetch()-> str:
    def custom_decoder(d):
        for key, value in d.items():
            if isinstance(value, str):
                try:
                    d[key] = parser.isoparse(value)
                except ValueError:
                    pass
        return d

    collection = db[request.args.get('collection', 'logs')]
    raw_aggs = request.args.get('aggs', "[]").replace("%20", "").replace("__DATEYEAR", datetime(datetime.now().year, 1, 1).isoformat()).replace("__DATEWEEK", (datetime.now() - timedelta(days=7)).isoformat())
    print(raw_aggs)
    aggs = json.loads(raw_aggs, object_hook=custom_decoder)
    res = collection.aggregate(aggs)
    data = list(res)
    if not data:
        return jsonify([])
    if "_id" in data[0]:
        for i in range(len(data)):
            data[i]["_id"] = str(data[i]["_id"])
    return jsonify(data)

@app.route('/log-session', methods=['POST'])
def log_session():
    """
    Exemple de log:
    {
        "ip":"127.0.0.1",
        "timestamp":"2025-03-29 09:46:49",
        "country":"FR",
        "mode":"solo",
        "word":"TRINITE",
        "time":10923,
        "score":110,
        "attemps":6,
        "count":2,
        "success":False
    }    
    """
    try:
        data = request.get_json()

        log = {
            "timestamp": datetime.now(timezone.utc),
            **data
        }

        # Récupérer le pays de l'utilisateur
        # Utilisation de ipinfo.io pour obtenir le pays à partir de l'IP
        if "ip" in data.keys():
            ip = data["ip"]
            res = requests.get(f"https://ipinfo.io/{ip}/json").json()
            log["country"] = res.get('country', None)

        print("Log reçu :", log)

        logs_collection.insert_one(log.copy())

        return jsonify({"status": "success", "log": log}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Configuration de APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_daily_word, 'interval', days=1, next_run_time=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))  # À partir du 13 mars 2025
    scheduler.start()
    get_daily_word()

    app.run(host="0.0.0.0", port=8000, debug=True)