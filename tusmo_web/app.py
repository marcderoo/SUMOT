from flask import Flask, render_template, send_file, redirect, url_for, jsonify, request
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

@app.route('/solo')
def solo():
    random_word = random.choice(dico).upper()  # Mot mystère
    return render_template('index.html', data=random_word)

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
