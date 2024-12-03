# Projet_Infra_Tusmo

## ** A FAIRE **
On trouvera ci-dessous la liste des tâches à effectuer avant la prochaine réunion : (Ajouter ✅ lorsque c'est fait, et ajouter ❌ lorsqu'il y a un problème)

- Conteneurisation : docker (MARC) ✅
  docker build -t tusmo_web .
  docker run -d -p 5000:5000 tusmo_web
  
- Tests unitaires js (MAX)
- Tests unitaires python (MERYEM)
- Typing (MERYEM)
- Documentation (python-doc / js-doc : directement dans le code : ca compile en markdown) (a la fin)
- ReadMe (a la fin)
- Aide de l'IA en mode solo (ARNAUD)
- IA ultime (MAX) ✅
  
- Revoir les defs 
- Idées d'amélioration (IA en moins de mots possibles / mots par thèmes / récompenses avec le score)

## **Description**
Ce projet vise à développer une version du jeu **Tusmo** qui propose une IA en aide ou à affronter. L'objectif est de fournir :
- Une **interface web** intuitive pour jouer.
- Un **solveur intelligent** capable de proposer des mots optimaux, en tenant compte des règles de couleurs (rouge, jaune, noir).
- Une IA à affronter au tour par tour, objectif de trouver en le moins de mots possibles.

Le projet a été conçu dans le cadre de la matière *Infrastructures et Systèmes Logiciels*.

---

## **Fonctionnalités prévues**
1. **Jeu via interface web :**
   - Les joueurs devinent un mot mystère en 6 essais.
   - Indication visuelle (rouge, jaune, noir) des lettres.

2. **Solveur IA :**
   - Algorithme basé sur la quantité d’information des mots.
   - Filtrage dynamique des propositions en fonction des retours.

---

## **Structure du projet**
tusmo-solver/
├── solver.py 
├── dictionnaire.txt
├── .gitignore
├── README.md
├tusmo_web/
├── app.py
├── static/
│   ├── styles.css
│   ├── script.js
│   └── images/
├── templates/
│   └── index.html
├── requirements.txt



---

## **Installation**

git clone https://github.com/username/tusmo-solver.git
cd tusmo-solver
pip install -r requirements.txt


## **Auteurs**
Arnaud Cournil
Maxime Chappuis
Meryem El Aissaoui
Marc Deroo

