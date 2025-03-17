from typing import List, Dict, Optional, Union
from flask import Flask, render_template, send_file, request
import random
import requests
from bs4 import BeautifulSoup
from functools import lru_cache
from apscheduler.schedulers.background import BackgroundScheduler
from unidecode import unidecode
from datetime import datetime, timedelta
import os

daily_word = "DEFAUT"

app = Flask(__name__)

os.chdir(os.path.dirname(__file__))

with open("small_dico.txt", 'r') as file:
    dico = [line.strip() for line in file]

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
            "x-magicapi-key": "cm85xxupg0008k003ggyouam3"
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

@app.route('/') 
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

if __name__ == '__main__':
    # Configuration de APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_daily_word, 'interval', days=1, next_run_time=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))  # À partir du 13 mars 2025
    scheduler.start()

    get_daily_word()

    app.run(host="0.0.0.0", port=5000, debug=True)