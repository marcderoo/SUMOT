from flask import Flask, render_template, send_file, request, redirect, url_for
import json
import random
import os

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

@app.route('/versus_ia')
def versus_ia():
    return render_template('versusia.html')

@app.route('/regles')
def regles():
    return render_template('regles.html')

@app.route('/dico/<filename>')
def get_dico(filename):
    return send_file('dico/' + filename)

if __name__ == '__main__':
    app.run(debug=True)
