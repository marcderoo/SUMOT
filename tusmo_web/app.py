from typing import List, Dict, Optional, Union
from flask import Flask, render_template, send_file, request
import random
import requests
from bs4 import BeautifulSoup
from functools import lru_cache

app: object = Flask(__name__)

with open("small_dico.txt", 'r') as file:
    dico: list[str] = [line.strip() for line in file]

with open("frequences_lettres.txt", "r") as file:
    frequences_lettres: dict[str, float] = {
        ligne.split(" : ")[0].strip(): float(ligne.split(" : ")[1].strip())
        for ligne in file if " : " in ligne
    }

# Route d'accueil
@app.route('/') 
def menu()-> str:
    return render_template('menu.html')

@app.route('/solo', methods=['POST', 'GET'])
def solo()-> str:
    score: int = 0
    count: int = 1
    
    if request.method == 'POST':
        score: int = request.form.get('score', 0, type=int)  # Récupération de 'score' depuis le formulaire
        count: int = request.form.get('count', 1, type=int)  # Récupération de 'count' depuis le formulaire

    random_word = random.choice(dico).upper()  # Mot mystère
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
        score = request.form.get('score', 0, type=int)  # Récupération de 'score' depuis le formulaire
        count = request.form.get('count', 1, type=int)  # Récupération de 'count' depuis le formulaire

    random_word = random.choice(dico).upper()  # Mot mystère
    return render_template('versusia.html', data={
        "word": random_word,
        "score": score,
        "count": count
    })

@app.route('/regles')
def regles()-> str:
    return render_template('regles.html')

@app.route('/dico/<filename>')
def get_dico(filename: str)-> Union[str, bytes]:
    return send_file('dico/' + filename)

@app.route('/def/<mot>')
def get_def(mot: str) -> str:
    """Récupère uniquement la définition principale pour le mot depuis le Wiktionnaire."""
    url: str = f"https://fr.wiktionary.org/wiki/{mot}"
    try:
        # Ajout d'un timeout pour éviter une requête qui traîne trop longtemps
        response: object = requests.get(url, timeout=5)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP

        soup: object = BeautifulSoup(response.text, "html.parser")
        definition: object = soup.find("ol")  # Recherche de la liste ordonnée des définitions

        if definition:
            premier_element: object = definition.find("li")  # Cherche le premier élément de la liste
            if premier_element:
                # Extraire la première ligne avant les retours à la ligne
                return premier_element.text.split("\n")[0].strip()
        return "err"  # Cas où aucune définition n'est trouvée
    except Exception as e:
        return "err"  # erreurs générales
    
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
    data: Dict[str, Union[int, str, Dict[str, Dict[str, Union[int, bool, List[int]]]]], List[Union[str, bool]], List[str]] = request.get_json()
    words: List[str] = [word.upper() for word in dico if len(word) == data["len"] and word[0].upper() == data["firstLetter"] and word not in data["history"]]

    filtred: List[str] = []
    for word in words:
        if difficulte > 0:
            countLetters: Dict[str, int] = {}
            goToNext: bool = False
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
        mot_final: str = max(mots_uniques or filtred , key=somme_frequences)
    else:
        mot_final: str = random.choice(filtred)

    return mot_final

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)