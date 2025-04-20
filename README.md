# **SUMOT** 

[![Build and Push Docker Image](https://github.com/marcderoo/SUMOT/actions/workflows/prod.yml/badge.svg)](https://github.com/marcderoo/SUMOT/actions/workflows/prod.yml)

## Améliorations dans le cadre du projet de 'Mise en Production'

**Parcours dashboard / Application Interactive**

- Mise en place des bonnes pratiques
  - Utilisation de linter automatisée (github action : 8.57/10 en moyenne) ✅
  - Structure Cookiecutter en migrant nos données sur S3 (SSPCLoud) et utilisation de secrets variables ✅
  - Ajout fichiers LICENSE (GNU) et .gitignore ✅
  - Adaptation des tests unitaires et mise en place sur Github Actions ✅
  - Amélioration continue de la qualité du code avec Pylint ✅

- Création d'un Dashboard Statique qui recueil des statistiques générales sur l'application ✅
- Création d'un mode "Mot Du Jour" qui s'update automatiquement en cherchant le mot dans le top tendance Twitter ✅
- Interfacer DOCKER avec GITHUB : l'image se créer et push automatiquement avec Github Actions ✅
- Industrialiser le déploiement en mode GitOps avec ArgoCD ✅
   - Le déploiement de l'application est controlé par un autre dépôt : https://github.com/marcderoo/SUMOT-deployment.git

---

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
pip install -r app/requirements.txt
```

Run the application locally (& Unit Tests):


```bash
python tests/start_app.py
```

Using Docker:


```bash
docker compose up -d --build
```

Run tests:


```bash
python tests/test_tusmo_app.py
```

## **Environment variables**

Create a `.env` file at the root of the project with the following variables:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
X-MAGICAPI-KEY=your_magicapi_key
MONGODB_URI=your_mongodb_connection_string
```

---

## **Overview** 
<p align="center">
    <img src="./app/static/menu.png" alt="Image 1" height="400" style="margin-right: 10px;">
    <img src="./app/static/versusia.png" alt="Image 2" height="400">
</p>

---

## **Application Features** 
The application includes a main menu with access to five distinct pages:
 
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

2. **Daily Word** :
  - A new challenge every day with a word selected from trending topics.
  
  - Same gameplay mechanics as Solo mode but with a shared word for all players.
  
  - Track your daily score and compare with friends.
 
3. **Versus AI** :
  - Duel mode where the player competes against the AI, taking turns to guess the word.

  - The starting player is chosen randomly.
 
  - AI difficulty is configurable with 4 levels: 
    - **Easy** : Only considers well-placed letters.
 
    - **Medium** : Considers well-placed and misplaced letters.
 
    - **Hard** : Includes absent letters in its strategy.
 
    - **Expert** : Optimally uses all information, maximizing letter frequencies while diversifying attempts.

4. **Dashboard** :
  - Analytical dashboard showing real-time statistics about the game usage.
  
  - Visualize key metrics like:
    - Number of unique users
    - Daily active users
    - Geographic distribution of players
    - Win rate against AI by difficulty level
    - Average time to guess words
    - Distribution of games by mode
    - Evolution of the number of games over time
  
  - All data is stored in MongoDB and aggregated for visualization.

5. **Rules** :
  - A detailed explanation of the game rules.

### Notes: 

- Words to guess are between 6 and 9 letters long and belong to a common word list to simplify the experience.

- The player can use any valid word from the dictionary for their attempts.

- The Daily Word feature uses Twitter trending topics to select words, ensuring they are current and relevant.

- All game statistics are stored in MongoDB for analysis and displayed in the dashboard.

---

## **MongoDB Integration**

The application uses MongoDB to store various statistics about gameplay:

1. **Data Collection**:
   - Every game played is logged with details about:
     - Game mode used
     - Time taken to complete
     - Number of attempts
     - Success/failure
     - User information (anonymous identifier)
     - Geographic data (country/region)

2. **Data Structure**:
   - Main collections:
     - `logs`: Raw game events
     - `users`: User information and aggregated statistics
     - `words`: Information about words used in the game
     - `daily_stats`: Aggregated daily statistics

3. **Dashboard Analytics**:
   - The dashboard uses aggregation pipelines to process and visualize:
     - User engagement metrics
     - Gameplay statistics
     - Performance trends over time
     - Geographic distribution of users

4. **Configuration**:
   - Connection is managed through the `MONGODB_URI` environment variable
   - Authentication is handled securely through the connection string

5. **Benefits**:
   - Real-time updates of gameplay statistics
   - Persistent storage of user progress
   - Data-driven game improvements based on analytics
   - Scalable solution for growing user base

---

## **Code Structure** 
The project is divided into three main parts:
 
1. **app** :
  - Contains the main application code.
  
  - **`app.py`** : Entry point for the Flask application.
  
  - **`templates/`** : HTML templates for the application's pages.
  
  - **`static/`** : Contains front-end files.
  
  - **`requirements.txt`** : List of Python dependencies.

2. **tests** :
  - Contains all unit tests and test utilities.
  
  - **`test_app.py`** : Unit tests for the Flask application.
  
  - **`test_tusmo_app.py`** : Script to run all unit tests.
  
  - **`start_app.py`** : Script to run tests and start the application.

3. **experiments** :
  - Contains experimental code and development trials.

### Running the application locally: 
 
- Execute `tests/start_app.py` after installing the dependencies via `app/requirements.txt`.

### Notes: 

- Unit tests are done automatically in github (with "Unit tests CI" workflow in the section Actions of the tab bar)
- The application can use local files or cloud storage (S3) based on environment configuration
- MongoDB connection requires proper environment variables to be set

---

## **Project Architecture** 

```
SUMOT/
├── .dockerignore                # Files to ignore in Docker builds
├── .gitignore                   # Files to ignore in Git
├── LICENSE                      # GNU License file
├── README.md                    # Main documentation
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Docker configuration
│
├── .github/                     # GitHub configuration
│   └── workflows/               # GitHub Actions
│       ├── docker-image.yml     # Docker workflow
│       ├── pylint.yml           # Pylint workflow
│       └── prod.yml             # Production workflow
├── app/                         # Main application
│   ├── __init__.py              # Package initialization
│   ├── app.py                   # Flask entry point
│   ├── compute_dico.py          # Dictionary processor
│   ├── frequences_lettres.txt   # Letter frequencies
│   ├── requirements.txt         # Python dependencies
│   ├── small_dico.txt           # Reduced dictionary
│   ├── vercel.json              # Vercel configuration
│   │
│   ├── dico/                # Dictionaries organized by letters and length
│   │   ├── A_6.txt          # Words starting with "A" and having 6 letters
│   │   └── ...              # Other dictionary files
│   │
│   ├── experiments/               # Experiments
│   │   ├── __init__.py              # Package initialization    
│   │   ├── dictionnaire.txt         # Raw dictionary
│   │   ├── mode_battleIA.py         # AI battle mode
│   │   ├── mode_battleIA_test.py    # Battle mode tests
│   │   ├── mode_duel.py             # Duel mode
│   │   ├── mode_duel_test.py        # Duel mode tests
│   │   ├── solveur.py               # Game solver
│   │   └── solveur_test.py          # Solver tests
│   │
│   ├── static/                  # Static files
│   │   ├── appUtils.js          # JavaScript utilities
│   │   ├── appUtils.md          # Utilities documentation
│   │   ├── confetti.js          # Confetti animation
│   │   ├── dashboard.css        # Dashboard styles
│   │   ├── dashboard.js         # Dashboard logic
│   │   ├── dashboard.webp       
│   │   ├── favicon.png          # Site icon
│   │   ├── menu.png             # Menu image
│   │   ├── noodles.webp         # Noodles image (score)
│   │   ├── script.js            # Main script
│   │   ├── script.md            # Main script documentation
│   │   ├── styles.css           # Main stylesheet
│   │   ├── versusia.png         # Versus AI image
│   │   ├── wallpaper.webp       # Background image
│   │   │
│   │   └── libs/                # External libraries
│   │       ├── chart.js         # Chart.js for graphs
│   │       ├── countries-50.json # Geographic data
│   │       ├── chartjs-chart-geo.js      
│   │       ├── iso-3166.json    # ISO country codes
│   │       ├── material-components-web.min.css
│   │       ├── normalize.min.css
│   │       ├── ods.css      
│   │       ├── ods-widgets.css  # Data widgets styles
│   │       ├── tailwindcss.js   # Tailwind CSS framework
│   │       └── theme.css        # Custom theme
│   │
│   └── templates/               # HTML templates
│       ├── daily.html           # Daily word page
│       ├── dashboard.html       # Analytics dashboard
│       ├── menu.html            # Main menu
│       ├── regles.html          # Game rules
│       ├── solo.html            # Solo mode
│       ├── table.html           
│       └── versusia.html        # Versus AI mode
│
├── deployment/                  # Kubernetes configuration
│   ├── deployment.yml           # Pods deployment
│   ├── ingress.yml              # Ingress configuration
│   └── service.yml              # Network service
│
│
├── tests/                       # Tests
│   ├── __init__.py              # Package initialization
│   ├── start_app.py             # App starter with tests
│   ├── test_app.py              # Flask tests
│   └── test_tusmo_app.py        # Global tests
│
└── utils/                       # Utilities
    └── mongo_logger.py          # MongoDB logging
```

---

## **Deployment** 

The application can be deployed in multiple ways:

1. **Local Development**:
   ```bash
   python tests/start_app.py
   ```

2. **Docker Container**:
   ```bash
   docker compose up -d --build
   ```

3. **Kubernetes on SSP Cloud**:
   - The application is configured for deployment on SSP Cloud's Kubernetes cluster
   - Deployment is managed through ArgoCD in GitOps style
   - Configurations are stored in a separate deployment repository

4. **CI/CD Pipeline**:
   - All code commits trigger automated tests and linting
   - The main branch builds and pushes Docker images automatically
   - The deployment repository pulls the latest image and updates the Kubernetes deployment

---

## **Contributors** 
- Maxime Chappuis
- Arnaud Cournil
- Marc Deroo
- Meryem El Aissaoui
- Laurent Vong