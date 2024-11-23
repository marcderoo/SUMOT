document.addEventListener('DOMContentLoaded', () => {
    // Vérification de la variable real_word
    if (!real_word || real_word.length === 0) {
        console.error("Le mot mystère n'a pas été transmis.");
        return;
    }

    console.log("Mot mystère reçu :", real_word);

    const confetti = new Confetti();
    const style = document.createElement('style');
    document.head.appendChild(style);

    const NBLETTERS = real_word.length;
    const NBTRY = 6;
    const FIRSTLETTER = real_word[0];
    let dico = [];
    let confirmed = false;
    let end = false;

    // Chargement du dictionnaire
    fetch(`dico/${FIRSTLETTER}_${NBLETTERS}.txt`)
        .then(response => {
            if (!response.ok) throw new Error('Erreur lors du chargement du dictionnaire.');
            return response.text();
        })
        .then(data => {
            dico = data.split("\r\n");
            console.log("Dictionnaire chargé :", dico);
        })
        .catch(error => {
            console.error('Erreur lors du fetch :', error);
        });

    // Configuration CSS dynamique
    const MAX = Math.max(NBLETTERS, NBTRY);
    style.innerHTML = `
        .grid-container {
            grid-template-columns: repeat(${NBLETTERS}, 1fr);
            grid-template-rows: repeat(${NBTRY}, 1fr);
            width: calc(${Math.ceil(90 / MAX) * NBLETTERS} * (100vmin - 160px) / 100);
            height: calc(${Math.ceil(90 / MAX) * NBTRY} * (100vmin - 160px) / 100);
        }
        .cell {
            font-size: ${Math.ceil(90 / MAX) * NBTRY / 12}vmin;
        }
    `;

    // Génération de la grille
    const container = document.querySelector('.grid-container');
    for (let i = 0; i < NBLETTERS * NBTRY; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        if (i === 0) cell.innerHTML = FIRSTLETTER;
        container.appendChild(cell);
    }

    // Fonction de vérification du mot
    function verify(written_word) {
        const res = [];
        const dic_real_word = real_word.split('').reduce((acc, char) => {
            acc[char] = (acc[char] || 0) + 1;
            return acc;
        }, {});

        for (let i = 0; i < written_word.length; i++) {
            if (written_word[i] === real_word[i]) {
                res.push(2);
                dic_real_word[real_word[i]] -= 1;
            } else {
                res.push(0);
            }
        }

        for (let i = 0; i < written_word.length; i++) {
            if (res[i] === 0 && dic_real_word[written_word[i]] > 0) {
                res[i] = 1;
                dic_real_word[written_word[i]] -= 1;
            }
        }

        // Met à jour les couleurs des lettres de l'alphabet
        updateAlphabetColor(written_word, res);

        return res;
    }

    // Gestion du clavier
    document.addEventListener('keydown', function(event) {
        const cells = Array.from(document.querySelectorAll("div.cell"));
        let lastFilledCell = null;

        for (let i = cells.length - 1; i >= 0; i--) {
            if (cells[i].innerHTML !== "") {
                lastFilledCell = { cell: cells[i], index: i };
                break;
            }
        }

        if (!end) {
            if (event.key.length === 1 && /[a-zA-Z]/.test(event.key)) {
                if ((lastFilledCell.index + 1) % NBLETTERS !== 0 || confirmed) {
                    cells[lastFilledCell.index + 1].innerHTML = event.key.toUpperCase();
                    confirmed = false;
                }
            } else if (event.key === "Backspace") {
                if (lastFilledCell && lastFilledCell.index % NBLETTERS !== 0) {
                    lastFilledCell.cell.innerHTML = "";
                }
            } else if (event.key === "Enter") {
                if ((lastFilledCell.index + 1) % NBLETTERS === 0) {
                    const word = cells.slice(lastFilledCell.index + 1 - NBLETTERS, lastFilledCell.index + 1)
                        .map(cell => cell.innerHTML).join("");

                    if (dico.includes(word.toLowerCase())) {
                        const res = verify(word);
                        for (let i = 0; i < res.length; i++) {
                            cells[lastFilledCell.index + 1 - NBLETTERS + i].classList.add(
                                res[i] === 2 ? "valid" : (res[i] === 1 ? "good" : "unvalid")
                            );
                        }

                        confirmed = true;
                        if (res.every(e => e === 2)) {
                            end = true;
                            confetti.launch();
                        } else {
                            cells[lastFilledCell.index + 1].innerHTML = FIRSTLETTER;
                        }
                    } else {
                        cells.slice(lastFilledCell.index + 1 - NBLETTERS, lastFilledCell.index + 1)
                            .forEach(elmt => elmt.classList.add("uncorrect"));

                        end = true;
                        setTimeout(() => {
                            cells.slice(lastFilledCell.index + 1 - NBLETTERS, lastFilledCell.index + 1).forEach(elmt => {
                                elmt.innerHTML = "";
                                elmt.classList.remove("uncorrect");
                            });
                            cells[lastFilledCell.index + 1 - NBLETTERS].innerHTML = FIRSTLETTER;
                            end = false;
                        }, 300);
                    }
                }
            } else {
                console.log(event.key);
            }
        }
    });

    // Génération des lettres de l'alphabet
    const alphabetContainer = document.querySelector('.alphabet-grid');
    const azerty = [
        "azertyuiop",
        "qsdfghjklm",
        "wxcvbn"
    ];

    azerty.forEach(row => {
        const rowContainer = document.createElement('div');
        rowContainer.classList.add('alphabet-row');

        row.split('').forEach(letter => {
            const letterCell = document.createElement('div');
            letterCell.classList.add('alphabet-cell');
            letterCell.textContent = letter;
            letterCell.setAttribute('data-letter', letter);
            rowContainer.appendChild(letterCell);
        });

        alphabetContainer.appendChild(rowContainer);
    });

    // Mise à jour des couleurs des lettres de l'alphabet
    function updateAlphabetColor(writtenWord, result) {
        const alphabetCells = document.querySelectorAll('.alphabet-cell');

        writtenWord.split('').forEach((letter, i) => {
            const letterCell = Array.from(alphabetCells)
                .find(cell => cell.getAttribute('data-letter') === letter.toLowerCase());

            if (letterCell) {
                if (result[i] === 2) {
                    letterCell.classList.remove('good', 'unvalid');
                    letterCell.classList.add('valid');
                } else if (result[i] === 1) {
                    if (!letterCell.classList.contains('valid')) {
                        letterCell.classList.remove('unvalid');
                        letterCell.classList.add('good');
                    }
                } else if (result[i] === 0) {
                    if (!letterCell.classList.contains('valid') && !letterCell.classList.contains('good')) {
                        letterCell.classList.add('unvalid');
                    }
                }
            }
        });
    }
});
