from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Liste des mots à deviner (utilise une liste simplifiée pour le moment)
mots = ["ecart", "panier", "chat", "sol", "belle"]

# Route d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour recevoir la réponse du joueur
@app.route('/verifier', methods=['POST'])
def verifier():
    mot_joueur = request.form['mot']
    mot_mystere = "ecart"  # Choisir le mot mystère (pour l'instant statique)
    
    # Logique de vérification du mot
    feedback = ""
    for i in range(len(mot_joueur)):
        if mot_joueur[i] == mot_mystere[i]:
            feedback += "🟥"  # Lettre bien placée (rouge)
        elif mot_joueur[i] in mot_mystere:
            feedback += "🟨"  # Lettre mal placée (jaune)
        else:
            feedback += "⬛"  # Lettre absente (noire)

    return render_template('index.html', feedback=feedback, mot_joueur=mot_joueur)

if __name__ == '__main__':
    app.run(debug=True)
