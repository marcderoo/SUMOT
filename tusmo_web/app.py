from flask import Flask, render_template, send_file, request
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

dico = []
with open("small_dico.txt", 'r') as file:
    dico = list(set([line.strip() for line in file if line.strip()]))

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


if __name__ == '__main__':
    app.run(debug=True)
