from flask import Flask, render_template, send_file, request
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

dico = []
with open("small_dico.txt", 'r') as file:
    dico = [line.strip() for line in file if line.strip()]

# Route d'accueil
@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/solo', methods=['POST', 'GET'])
def solo():
    score = 0
    count = 1
    
    if request.method == 'POST':
        score = request.form.get('score', 0, type=int)  # Récupération de 'score' depuis le formulaire
        count = request.form.get('count', 1, type=int)  # Récupération de 'count' depuis le formulaire

    random_word = random.choice(dico).upper()  # Mot mystère
    return render_template('index.html', data={
        "word": random_word,
        "score": score,
        "count": count
    })

@app.route('/versus_ia', methods=['POST', 'GET'])
def versus_ia():
    score = 0
    count = 1
    
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
def regles():
    return render_template('regles.html')

@app.route('/dico/<filename>')
def get_dico(filename):
    return send_file('dico/' + filename)

@app.route('/def/<mot>')
def get_def(mot):
    """Récupère uniquement la définition principale pour le mot depuis le Wiktionnaire."""
    url = f"https://fr.wiktionary.org/wiki/{mot}"
    try:
        # Ajout d'un timeout pour éviter une requête qui traîne trop longtemps
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP

        soup = BeautifulSoup(response.text, "html.parser")
        definition = soup.find("ol")  # Recherche de la liste ordonnée des définitions

        if definition:
            premier_element = definition.find("li")  # Cherche le premier élément de la liste
            if premier_element:
                # Extraire la première ligne avant les retours à la ligne
                return premier_element.text.split("\n")[0].strip()
        return "err"  # Cas où aucune définition n'est trouvée
    except Exception as e:
        return f"err"  # erreurs générales
    

@app.route('/ia', methods=['POST'])
def bot_proposition_difficile():
    """
        Le bot utilise toutes les couleurs pour filtrer les mots possibles, sans gestion de lettres consommées.
        data["len"] : longueur du mot
        data["firstLetter"] : première lettre du mot (en majuscule)
        data["validLetters"] : liste qui contient la position des lettres bien placés au bon endroit de la forme, par exemple pour un mot de 4 lettre avec un L bien placé à la première position et un n a la troisième, ça donnerait : ["L", False, "N", "G"]
        goodLetter : liste de tuple qui contient les lettres mal placées et leur mauvaise position passée de la forme par exemple : 
            [("A", [1, 3]), ("B", [1, 5])]
            Cet exemple signifie que A placé en 1 est une bonne lettre mais mal placé, A placé en 3 est une bonne lettre mais mal placé, etc ... 
        unvalidLetter : list des lettres non valides 
    """
    data = request.get_json()
    words = []
    with open("small_dico.txt", 'r') as file:
        words = [line.strip().upper() for line in file if len(line.strip()) == data["len"] and line[0].upper() == data["firstLetter"]]

    filtred = []
    for word in words:
        data["goodLetters"] = data["goodLetters"].copy()
        for i in range(data["len"]):
            if data["validLetters"][i]:
                if word[i] == data["validLetters"][i]:
                    continue
                else:
                    break

            if word[i] in list(map(lambda x : x[1], data["goodLetters"])):
                for j in range(len(data["goodLetters"])):
                    if data["goodLetters"][j] == word[i]:
                        del data["goodLetters"][j]

            if word[i] == data["unvalidLetters"]:
                break

            if i == data["len"] - 1 and len(data["goodLetters"]) == 0:
                filtred.append(word)

    return random.choice(filtred)

if __name__ == '__main__':
    app.run(debug=True)