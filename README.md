# **SUMOT**

## Idées amélioration dans le cadre de 'Mise en Production'

- Mise en place des bonnes pratiques
  - pylint sur les .py amélioration de 5/10 à 8/10 en moyenne (le prof a dit que 7 c'est très bien) ✅
- fichiers LICENSE (GNU) et .gitignore ✅
- architecture cookiecutter --> pbs tests unitaires 
- Mettre les données sur S3 (SSPCLoud) 
- Interfacer DOCKER avec GITHUB ✅ [![Build and Push Docker Image](https://github.com/marcderoo/SUMOT/actions/workflows/prod.yml/badge.svg)](https://github.com/marcderoo/SUMOT/actions/workflows/prod.yml)
- Industrialiser le déploiement en mode GitOps avec ArgoCD
- Automatiser l’ingestion des données en entrée pour que le site web se mette à jour régulièrement 
- DAHSBOARD : Gérer le monitoring de l’application : logs, métriques de suivi des performances, etc. 

---

- Ajouter un mot du jour qui se base sur un mot tendance google ✅
- Chronométrer la résolution du mot du jour ✅ 
- Customiser : fonds d'écrans, thèmes de mots (films, animaux, gateaux, ...)
- Bonus : pourvoir comparer avec ses amis (bouton partager)
- Bonus : mettre une version en anglais (= customiser CSS etc.)

## **Description of SUMOT** 

This project aims to develop a game inspired by **Tusmo** , **Sutom** , and the TV game show **Motus** . Our version introduces a mode where players compete against an AI with varying difficulty levels. This AI is also available as a helper in Solo mode.
The objectives are:
 
- To deploy the game with an intuitive and smooth **web interface** .
 
- To develop an **AI**  capable of suggesting optimal words by considering well-placed, misplaced, and absent letters in the word.

- To display a definition of the word once it is guessed.  

This project was developed as part of the *Infrastructures et systèmes logiciels* course in the ENSAE Master's Degree in Data Science.

---

## **Installation and Prerequisites** 
Clone this repository:


```bash
git clone https://github.com/username/Projet_Infra_Tusmo.git \
cd Projet_Infra_Tusmo
```

Install the necessary dependencies:


```bash
pip install -r requirements.txt
```

Run the application locally (& Unit Tests):


```bash
python start_app.py
```

Using Docker:


```bash
docker compose up -d --build
```

Run tests:


```bash
python test_tusmo_app.py
```


---

## **Overview** 
<p align="center">
    <img src="./app/static/menu.png" alt="Image 1" height="400" style="margin-right: 10px;">
    <img src="./app/static/versusia.png" alt="Image 2" height="400">
</p>

---

## **Application Features** 
The application includes a main menu with access to three distinct pages:
 
1. **Solo** :
  - Classic gameplay where the player must guess the word in up to 6 attempts.

  - The goal is to achieve the longest streak to accumulate a high score.

  - Scores decrease based on the number of attempts needed to guess the word.
 
  - Hints are available in exchange for points: 
    - **100 points** : The expert AI suggests a word.
 
    - **60 points** : A well-placed letter is revealed.
 
    - **30 points** : A letter absent from the word is removed.
 
  - **Color codes** : 
    - **Green** : Well-placed letter.
 
    - **Yellow** : Correct letter but misplaced.
 
    - **Greyed out (keyboard)** : Letter absent from the word.
 
  - **Interactive keyboard** : A visual keyboard helps track letters and allows gameplay on mobile devices.
 
2. **Versus AI** :
  - Duel mode where the player competes against the AI, taking turns to guess the word.

  - The starting player is chosen randomly.
 
  - AI difficulty is configurable with 4 levels: 
    - **Easy** : Only considers well-placed letters.
 
    - **Medium** : Considers well-placed and misplaced letters.
 
    - **Hard** : Includes absent letters in its strategy.
 
    - **Expert** : Optimally uses all information, maximizing letter frequencies while diversifying attempts.
 
3. **Rules** :
  - A detailed explanation of the game rules.

### Notes: 

- Words to guess are between 6 and 9 letters long and belong to a common word list to simplify the experience.

- The player can use any valid word from the dictionary for their attempts.


---

## **Code Structure** 
The project is divided into two main parts:
 
1. **Experiments** :
  - Contains experimental code and development trials.
 
2. **Root** :
  - Includes components needed to run the application.
 
  - **`app.py`** : Entry point for the Flask application.
 
  - **`requirements.txt`** : List of Python dependencies.

  - **`start_app.py`** : Check validity of unit tests and start the Flask application.
 
  - **`templates/`** : HTML templates for the application's pages.
 
  - **`static/`** : Contains front-end files: 
    - **CSS** : Style management.
 
    - **JavaScript** : Game logic and interactivity ([Documentation (JSDoc)](/doc.md) ).
 
    - **`dico/`** : Includes dictionaries sorted by initial letter and word length.

### Running the application locally: 
 
- Execute `start_app.py` after installing the dependencies via `requirements.txt`.

### Notes: 

- Unit tests are done automatically in github (with "Unit tests CI" workflow in the section Actions of the tab bar)

---

## **Project Architecture** 

```
SUMOT/
├── .dockerignore            # List of files/folders to exclude from the Docker image
├── app.py                   # Main entry point of the Flask application
├── compute_dico.py          # Script for generating or manipulating dictionaries
├── dictionnaire_clean.txt   # Cleaned dictionary used by the project
├── doc.md                   # Additional project documentation
├── docker-compose.yml       # Docker Compose configuration for deployment
├── Dockerfile               # Docker configuration to build the image
├── frequences_lettres.txt   # File containing letter frequencies
├── menu.png                 # Image used in the README
├── README.md                # Main documentation (this file)
├── requirements.txt         # List of Python dependencies
├── small_dico.txt           # Reduced version of the dictionary for using frequents words in the game
├── start_app.py             # Script to start the application with all Unit tests
├── test_app.py              # Unit tests for the Flask application
├── test_tusmo_app.py        # Script to start only all Unit tests
├── vercel.json              # Configuration for deployment on Vercel
├── versusia.png             # Another image used in the README
├── dico/                    # Dictionaries organized by letters and length
│   ├── A_6.txt              # Words starting with "A" and having 6 letters
│   ├── A_7.txt              # Words starting with "A" and having 7 letters
│   ├── A_8.txt              # Words starting with "A" and having 8 letters
│   ├── A_9.txt              # Words starting with "A" and having 9 letters
│   ├── B_6.txt              # Words starting with "B" and having 6 letters
│   ├── ...
│   └── Z_9.txt              # Words starting with "Z" and having 9 letters
├── static/                  # Static files (CSS, JS, images)
│   ├── appUtils.js          # Utility library
│   ├── appUtils.md          # Documentation for appUtils.js
│   ├── confetti.js          # JavaScript logic for displaying victory confetti
│   ├── confetti.md          # Documentation for confetti.js
│   ├── favicon.png          # Application icon
│   ├── noodles.webp          # Vector image of a bowl of noodles
│   ├── script.js            # Main JavaScript logic
│   ├── script.md            # Documentation for script.js
│   ├── styles.css           # Main stylesheet
│   └── wallpaper.webp        # Background image for the application
├── templates/               # HTML templates for views
│   ├── menu.html            # Game homepage with the menu
│   ├── regles.html          # Page explaining the rules
│   ├── solo.html            # Interface for solo game mode
│   └── versusia.html        # Interface for the game mode against Artificial Intelligence
├── experiments/             # Experimental scripts and features
│   ├── dictionnaire.txt     # Raw dictionary
|   ├── mode_battleIA_test.py# Unit tests for mode_battleIA.py
│   ├── mode_battleIA.py     # Battle mode against an AI
│   ├── mode_duel_test.py    # Unit tests for mode_duel.py
│   ├── mode_duel.py         # Duel mode between players
|   ├── solveur_test.py      # Unit tests for solveur.py
│   └── solveur.py           # Solver for the game
```


---

## **Contributors** 
- Maxime Chappuis

- Arnaud Cournil

- Marc Deroo

- Meryem El Aissaoui
