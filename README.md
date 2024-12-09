# **SUMOT**


## **A FAIRE**
On trouvera ci-dessous la liste des tâches à effectuer avant la prochaine réunion : (Ajouter ✅ lorsque c'est fait, et ajouter ❌ lorsqu'il y a un problème)

- Conteneurisation : docker (MARC) ✅\
  docker build -t tusmo_web . \
  docker run -d -p 5000:5000 tusmo_web
\
- Déploiement (Vercel : https://vercel.com/marcderoos-projects/sumot) ✅
\
- Documentation (python-doc / js-doc) (MARC)
- ReadMe (MARC) ✅ (A UPDATE régulièrment)
\  
- Tests unitaires js (MAX)
- IA ultime (MAX) ✅
\ 
- Tests unitaires python (MERYEM)
- Typing (MERYEM)✅
\
- Aide de l'IA en mode solo (ARNAUD)✅
- Shop 
- Revoir les defs 
- Idées d'amélioration (IA en moins de mots possibles✅ / mots par thèmes)



## **Description de SUMOT**
Ce projet vise à développer un jeu inspiré de **Tusmo**, **Sutom** ou encore le jeu télévisé **Motus**. L'ajout de notre version est qu'elle propose un mode contre une IA à affronter selon différents niveaux de difficultés. Cette IA est aussi disponible en aide dans le mode Solo. De plus, un système de récompense est mis en place, ces dernières permettent de personnaliser son décor et son sumo.\

L'objectif est de :
- déployer le jeu avec une **interface web** intuitive et fluide.
- développer une **IA** capable de proposer des mots optimaux, en tenant compte des lettres bien placées, mal placées et non existantes dans le mot.
- proposer un **sytème de récompense** et de **personnalisation** de son jeu.

Ce projet a été conçu dans le cadre de la matière *Infrastructures et Systèmes Logiciels* du Mastère Spécialisé Data Science de l'ENSAE.


## **Installation et prérequis**
Cloner ce dépot :
```bash
git clone https://github.com/username/Projet_Infra_Tusmo.git \
cd Projet_Infra_Tusmo
```

Installer les dépendances nécessaires :
```bash
pip install -r requirements.txt
```

Lancer l'application localement :
```bash
python app.py
```

Docker :
```bash
docker build -t tusmo_web .
docker run -d -p 5000:5000 tusmo_web
```

Tests :
```bash
python -m unittest discover tests
```

## **Aperçu**
<div style="display: flex; justify-content: space-around;">
    <img src="https://github.com/user-attachments/assets/82385267-01a7-4deb-a0eb-a66ea6b5c085" alt="Image 1" width="300" style="margin-right: 10px;">
    <img src="https://github.com/user-attachments/assets/d9339eb4-8469-415f-94ad-bb9f0fc06932" alt="Image 2" width="300">
</div>



## **Architecture du projet**
PROJET_INFRA_TUSMO/ \
├── tusmo_web/ \
│   ├── app.py                   # Main Flask application entry point \
│   ├── requirements.txt         # Python dependencies \
│   ├── Dockerfile \
│   ├── .dockerignore \
│   ├── vercel.json \
│   ├── small_dico.txt \
│   ├── frequences_lettres.txt \
│   ├── compute_dico.py \
│   ├── static/                  # Static files (CSS, JS, images, fonts)\
│   │   ├── styles.css           # Main stylesheet for the game\
│   │   ├── script.js            # Core JavaScript logic\
│   │   ├── images/              # Game assets (icons, backgrounds, etc.)\
│   │   └── fonts/               # Custom fonts for UI design\
│   ├── templates/               # HTML templates for rendering views\
│   │   └── index.html           # Main game interface\
│   ├── tests/                   # Unit and integration tests\
│   │   └── test_app.py          # Flask app test cases\
│   ├── README.md                # Project documentation\
│   ├── solveur.py\
│   ├── mode_duel.py\
│   ├── mode_battleIA.py\
│   ├── dictionnaire.txt\
│   ├── dictionnaire_clean.txt\
│   ├── freq_lettre_chat_gpt.txt\
│   └── .gitignore               # Files and folders excluded from Git\



## **Contributeurs**
Chappuis Maxime\
Cournil Arnaud\
Deroo Marc\
El Aissaoui Meryem


