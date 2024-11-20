from flask import Flask, render_template, send_file
import random

app = Flask(__name__)

dico = []
with open("dictionnaire_clean.txt", 'r') as file:
    dico = list(set([line.strip() for line in file if line.strip()]))

# Route d'accueil
@app.route('/')
def index():
    return render_template('index.html', data=random.choice(dico).upper())

@app.route('/dico/<filename>')
def get_dico(filename):
    # Assurez-vous que le fichier est dans un répertoire spécifique, ici par exemple 'dico_files'
    return send_file('dico/' + filename)

if __name__ == '__main__':
    app.run(debug=True)