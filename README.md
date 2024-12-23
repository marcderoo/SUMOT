# **SUMOT**

## **Description of SUMOT** 

This project aims to develop a game inspired by **Tusmo** , **Sutom** , and the TV game show **Motus** . Our version introduces a mode where players compete against an AI with varying difficulty levels. This AI is also available as a helper in Solo mode.
The objectives are:
 
- To deploy the game with an intuitive and smooth **web interface** .
 
- To develop an **AI**  capable of suggesting optimal words by considering well-placed, misplaced, and absent letters in the word.

- To display a definition of the word once it is guessed.
This project was developed as part of the *Infrastructures and Software Systems* course in the ENSAE Master's Degree in Data Science.

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

## **Overview** <div style="display: flex; justify-content: space-around;">
    <img src="https://github.com/user-attachments/assets/82385267-01a7-4deb-a0eb-a66ea6b5c085" alt="Image 1" width="300" style="margin-right: 10px;">
    <img src="https://github.com/user-attachments/assets/d9339eb4-8469-415f-94ad-bb9f0fc06932" alt="Image 2" width="300">
</div>

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

  - **`start_app.py`** : Start Flask application after Unit Tests.
 
  - **`templates/`** : HTML templates for the application's pages.
 
  - **`static/`** : Contains front-end files: 
    - **CSS** : Style management.
 
    - **JavaScript** : Game logic and interactivity ([Documentation (JSDoc)](https://chatgpt.com/doc.md) ).
 
    - **`dico/`** : Includes dictionaries sorted by initial letter and word length.

### Running the application locally: 
 
- Execute `start_app.py` after installing the dependencies via `requirements.txt`.


---

## **Project Architecture** 

```php
PROJET_INFRA_TUSMO/
├── app.py                   # Main Flask application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile
├── .dockerignore
├── vercel.json
├── small_dico.txt
├── frequences_lettres.txt
├── compute_dico.py
├── static/                  # Static files (CSS, JS, images, fonts)
│   ├── styles.css           # Main stylesheet for the game
│   ├── script.js            # Core JavaScript logic
│   ├── images/              # Game assets (icons, backgrounds, etc.)
│   └── fonts/               # Custom fonts for UI design
├── templates/               # HTML templates for rendering views
│   └── index.html           # Main game interface
├── tests/                   # Unit and integration tests
│   └── test_app.py          # Flask app test cases
├── README.md                # Project documentation
├── experiments/
│   ├── solveur.py
│   ├── mode_duel.py
│   ├── mode_battleIA.py
│   └── dictionnaire.txt
```


---

## **Contributors** 
- Maxime Chappuis

- Arnaud Cournil

- Marc Deroo

- Meryem El Aissaoui