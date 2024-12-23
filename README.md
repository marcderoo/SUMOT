# **SUMOT**

## **Description de SUMOT**
Ce projet vise à développer un jeu inspiré de **Tusmo**, **Sutom** ou encore du jeu télévisé **Motus**. L'ajout de notre version est qu'elle propose un mode contre une IA à affronter selon différents niveaux de difficultés. Cette IA est aussi disponible en aide dans le mode Solo. \

L'objectif est de :
- déployer le jeu avec une **interface web** intuitive et fluide.
- développer une **IA** capable de proposer des mots optimaux, en tenant compte des lettres bien placées, mal placées et non existantes dans le mot.
- proposer une définition du mot quand ce dernier est trouvé.

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
python start_app.py
```

Docker :
```bash
docker compose up -d --build
```

Tests :
```bash
python test_tusmo_app.py
```


## **Aperçu**
<div style="display: flex; justify-content: space-around;">
    <img src="https://github.com/user-attachments/assets/82385267-01a7-4deb-a0eb-a66ea6b5c085" alt="Image 1" width="300" style="margin-right: 10px;">
    <img src="https://github.com/user-attachments/assets/d9339eb4-8469-415f-94ad-bb9f0fc06932" alt="Image 2" width="300">
</div>


## **Fonctionnement de l'application**

L'application propose un menu principal avec accès à trois pages distinctes :

1. **Solo** : 
   - Mode de jeu classique où le joueur doit trouver le mot en 6 essais maximum.
   - L'objectif est de réaliser la plus longue série possible pour accumuler un score élevé.
   - Les scores sont dégressifs selon le nombre d'essais nécessaires pour trouver le mot.
   - Des aides sont disponibles en échange de points :
     - **100 points** : Proposition d’un mot par l'IA experte.
     - **60 points** : Révélation d'une lettre bien placée.
     - **30 points** : Suppression d'une lettre absente du mot.
   - **Code couleur** :
     - **Vert** : Lettre bien placée.
     - **Jaune** : Lettre présente mais mal placée.
     - **Effacé (clavier du jeu)** : Lettre absente du mot.
   - **Clavier interactif** : Un clavier visuel facilite le suivi des lettres et permet de jouer sur téléphone.

2. **Versus IA** :
   - Mode de jeu en duel contre l'IA, où chaque joueur tente de trouver le mot en premier, tour par tour.
   - Le joueur débutant est tiré au sort.
   - Difficulté de l'IA configurable avec 4 niveaux :
     - **Facile** : Utilisation des lettres bien placées uniquement.
     - **Moyen** : Utilisation des lettres bien placées et mal placées.
     - **Difficile** : Ajout de la prise en compte des lettres absentes.
     - **Experte** : Utilisation optimale de toutes les informations, maximisant les fréquences de lettres tout en diversifiant les essais.

3. **Règles** :
   - Contient un rappel détaillé des règles du jeu.

### Remarques :
- Les mots à trouver ont entre 6 et 9 lettres et appartiennent à une liste de mots courants pour simplifier l'expérience.
- Le joueur peut entrer n'importe quel mot du dictionnaire pour ses essais.

---

## **Fonctionnement du code**

Le projet est divisé en deux grandes parties :

1. **Experiments** :
   - Contient les codes expérimentaux et les essais réalisés lors du développement.

2. **Web** :
   - Regroupe les éléments nécessaires pour faire tourner l'application. 
   - **`app.py`** : Point d’entrée de l’application Flask.
   - **`requirements.txt`** : Liste des dépendances Python.
   - **`templates/`** : Regroupe les interfaces HTML pour chaque page de l'application.
   - **`static/`** : Contient les fichiers front-end :
     - **CSS** : Gestion du style.
     - **JavaScript** : Logique et interactivité du jeu.
   - **Dossier `dico/`** : Inclut les dictionnaires, triés par lettre initiale et longueur des mots.

### Lancer l'application localement :
- Exécutez `app.py` après avoir installé les dépendances via `requirements.txt`.



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


