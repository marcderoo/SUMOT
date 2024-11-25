const confetti = new Confetti();

const style = document.createElement('style');
document.head.appendChild(style);

let NBLETTERS = real_word.length;
const NBTRY = 6;
let FIRSTLETTER = real_word[0];

let dico = [];

let confirmed = false;
let end = false;
let validLetters = [];

const anecdotes = [
    '"Motus" a été créé par Thierry Beccaro, le célèbre animateur français. L’émission a été lancée en 1990 et a rencontré un grand succès grâce à son concept à la fois simple et stimulant. L’émission a duré plusieurs années, avec des saisons ponctuées de rebondissements et de surprises.',
    "Le concept de \"Motus\" est inspiré de celui du jeu de société Mastermind, où il faut deviner un code de couleurs. Dans \"Motus\", le défi est de deviner un mot de 5 ou 6 lettres en un nombre limité d'essais",
    'Au-delà de l’aspect télévisé, "Motus" est un jeu populaire dans les foyers français, avec des versions adaptées pour les jeux de société. Les familles adorent se défier en devinant des mots, et cela a renforcé la popularité du programme en dehors du petit écran.',
    "La plus grosse cagnotte de l'histoire de \"Motus\" est de 17 600 €7 (soit 22 émissions sans une Super partie gagnée)."
]
let def =  anecdotes[Math.floor(Math.random() * anecdotes.length)];

fetch(`def/${real_word.toLowerCase()}`)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.text();
  })
  .then(data => {
    if(data != "err"){
        def = `${real_word.charAt(0).toUpperCase() + real_word.slice(1).toLowerCase()} : ${data.toLowerCase()}`;
    }
  })

fetch(`dico/${FIRSTLETTER}_${NBLETTERS}.txt`)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.text();
  })
  .then(data => {
    dico = data.split("\r\n");
    console.log(dico);
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });

function verify(written_word){
    let res = []

    dic_real_word = real_word.split('').reduce((acc, char) => {
        acc[char] = (acc[char] || 0) + 1;
        return acc;
      }, {});

    for(let i = 0; i < written_word.length; i++){
        if(written_word[i] == real_word[i]){
            res.push(2);
            dic_real_word[real_word[i]] -= 1;
        } else {
            res.push(0);
        }
    }
    for(let i = 0; i < written_word.length; i++){
        if(res[i] == 0 && written_word[i] in dic_real_word && dic_real_word[written_word[i]] > 0){
            res[i] = 1;
            dic_real_word[written_word[i]] -= 1;
        }
    }
    return res;
}

document.addEventListener('DOMContentLoaded', () => {
    // Ajouter des règles CSS à l'élément <style>
    style.sheet.insertRule(`
        .grid-container {
            grid-template-columns: repeat(${NBLETTERS}, 1fr); /* 7 colonnes égales */
            grid-template-rows: repeat(${NBTRY}, 1fr);   /* 6 lignes égales */
        }`, 0);

    // Sélection du conteneur de la grille
    const container = document.querySelector('.grid-container');

    let lastCell = null;
  
    // Générer les NBLETTERS x NBTRY cellules
    for (let i = 0; i < NBLETTERS * NBTRY; i++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      if (i === 0){
        cell.innerHTML = FIRSTLETTER;
        validLetters.push(FIRSTLETTER);
      } else if (i < NBLETTERS) {
        validLetters.push(false);
      }
      container.appendChild(cell);
      lastCell = cell;
    }

    const updateFontSize = (first = false, cell = lastCell, grid = true) => {
        const cellWidth = cell.offsetWidth; // Largeur du conteneur
        const fontSize = cellWidth * 3 / 8; // 50% de la largeur du conteneur
        const idx = grid ? 1 : 2;
        const class_ = grid ? "cell" : "alphabet-cell";

        if(!first){
            style.sheet.deleteRule(idx);
        }

        style.sheet.insertRule(`
        .${class_} {
            font-size : ${fontSize}px
        }`, idx);
    };
    const resizeObserver = new ResizeObserver(() => {
        updateFontSize(); // Appelle la mise à jour à chaque changement de taille
    });
    resizeObserver.observe(lastCell);
    updateFontSize(true);

    // Génération des lettres de l'alphabet
    const alphabetContainer = document.querySelector('.alphabet-grid');
    const azerty = [
        'AZERTYUIOP',
        'QSDFGHJKLM',
        'WXCVBN'
    ];
    let lastCellAlphabet = null;

    azerty.forEach(row => {
        const rowContainer = document.createElement('div');
        rowContainer.classList.add('alphabet-row');

        row.split('').forEach(letter => {
            const letterCell = document.createElement('div');
            letterCell.classList.add('alphabet-cell');
            letterCell.textContent = letter;
            letterCell.setAttribute('data-letter', letter);
            rowContainer.appendChild(letterCell);
            lastCellAlphabet = letterCell;
        });

        alphabetContainer.appendChild(rowContainer);
    });

    const resizeObserverAlphabet = new ResizeObserver(() => {
        updateFontSize(false, lastCellAlphabet, false); // Appelle la mise à jour à chaque changement de taille
    });
    resizeObserverAlphabet.observe(lastCellAlphabet);
    updateFontSize(true, lastCellAlphabet, false);
});

document.addEventListener('keydown', function(event) {
    const cells = Array.from(document.querySelectorAll("div.cell"));
    let cellBeforeFirstEmptyCell = null;
    for (let i = 0; i < cells.length; i++) {
        if (cells[i].innerHTML == "" || cells[i].classList.contains("placeholder")) {
            cellBeforeFirstEmptyCell = { cell: cells[i - 1], index: i - 1 };
            break;
        }
    }

    if(!end){
        if (event.key.length === 1 && /[a-zA-Z]/.test(event.key)) {
            if((cellBeforeFirstEmptyCell.index + 1) % NBLETTERS !== 0 || confirmed){
                if(cellBeforeFirstEmptyCell.index % NBLETTERS !== 0 || cells[cellBeforeFirstEmptyCell.index].innerHTML !== event.key.toUpperCase()){
                    if(cells[cellBeforeFirstEmptyCell.index + 1].innerHTML != event.key.toUpperCase()){
                        cells[cellBeforeFirstEmptyCell.index + 1].classList.remove("valid");
                    }

                    cells[cellBeforeFirstEmptyCell.index + 1].classList.remove("placeholder");
                    cells[cellBeforeFirstEmptyCell.index + 1].innerHTML = event.key.toUpperCase();
                    confirmed = false;
                }
            }
        } else if (event.key == "Backspace"){
            if (cellBeforeFirstEmptyCell && cellBeforeFirstEmptyCell.index % NBLETTERS !== 0) {
                if(validLetters[cellBeforeFirstEmptyCell.index % NBLETTERS]){
                    cells[cellBeforeFirstEmptyCell.index].innerHTML = validLetters[cellBeforeFirstEmptyCell.index % NBLETTERS];
                    cells[cellBeforeFirstEmptyCell.index].classList.add("valid");
                    cells[cellBeforeFirstEmptyCell.index].classList.add("placeholder");
                } else {
                    cells[cellBeforeFirstEmptyCell.index].innerHTML = "";
                }
            }
        } else if (event.key == "Enter"){
            if ((cellBeforeFirstEmptyCell.index + 1) % NBLETTERS === 0) {
                const word = cells.slice(cellBeforeFirstEmptyCell.index + 1 - NBLETTERS, cellBeforeFirstEmptyCell.index + 1).map(cell => cell.innerHTML).join("");
                if(dico.includes(word.toLowerCase())){
                  const res = verify(word);
                  for(let i = 0; i < res.length; i++){
                      cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS + i].classList.add(res[i] === 2 ? "valid" : (res[i] === 1 ? "good" : "unvalid"));
                      const alphabetLetter = document.querySelector(`div.alphabet-cell[data-letter="${cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS + i].innerHTML}"`);
                      if(res[i] == 2){
                        validLetters[i] = cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS + i].innerHTML;
                        alphabetLetter.classList.remove("good");
                        alphabetLetter.classList.add("valid");
                      }
                      else if (res[i] == 1 && !alphabetLetter.classList.contains("valid")){
                        alphabetLetter.classList.add("good");
                      }
                  }

                  confirmed = true;
                  if(res.every(e => e === 2)){
                      end = true;
                      confetti.launch();
                      
                      count += 1;
                      score += 100 - Math.floor(cellBeforeFirstEmptyCell.index / NBLETTERS) * 10;

                      const dialog = document.createElement("dialog");
                      dialog.innerHTML = `<h2 style="margin-top: 0px;">Le saviez-vous ?</h2>
                        ${def}<br><br>
                        <div class="
                            next-button
                        " onclick=document.getElementById("form-end").submit()>Mot Suivant <span style="
                            border-style: solid;
                            border-width: 0.25em 0.25em 0 0;
                            content: '';
                            display: inline-block;
                            height: 0.45em;
                            position: relative;
                            top: 0.20em;
                            transform: rotate(45deg);
                            vertical-align: top;
                            width: 0.45em;
                            left: 0em;
                        "></span></div><br><br>`

                      document.body.appendChild(dialog);

                      dialog.showModal();

                        const form = document.createElement('form');
                        form.method = 'POST';
                        form.id = 'form-end';
                        form.action = window.location.href;
                        form.hidden = true;

                        const countInput = document.createElement('input');
                        countInput.type = 'hidden';
                        countInput.name = 'count';
                        countInput.id = 'count';
                        countInput.value = count; 

                        const scoreInput = document.createElement('input');
                        scoreInput.type = 'hidden';
                        scoreInput.name = 'score';
                        scoreInput.id = 'score';
                        scoreInput.value = score; 

                        form.appendChild(countInput);
                        form.appendChild(scoreInput);

                        document.body.appendChild(form);

                        dialog.addEventListener('keydown', function(event) {
                            if(event.key == "Enter"){
                                form.submit();
                            }
                        })

                  } else {
                    for(let i = 0; i < res.length; i++){
                        if(validLetters[i]){
                            cells[cellBeforeFirstEmptyCell.index + 1 + i].innerHTML = validLetters[i];
                            cells[cellBeforeFirstEmptyCell.index + 1 + i].classList.add("valid");
                            cells[cellBeforeFirstEmptyCell.index + 1 + i].classList.add("placeholder");
                        }                                          
                    }
                    cells[cellBeforeFirstEmptyCell.index + 1].classList.remove("placeholder");
                  }
                } else {
                  cells.slice(cellBeforeFirstEmptyCell.index + 1 - NBLETTERS, cellBeforeFirstEmptyCell.index + 1).forEach(elmt => elmt.classList.add("uncorrect"));
                  end = true;
                  setTimeout(function(){
                    for(let i = 0; i < NBLETTERS; i++){
                        cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS + i].classList.remove("uncorrect");
                        cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS + i].innerHTML = "";

                        if(validLetters[i]){
                            cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS + i].innerHTML = validLetters[i];
                            cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS + i].classList.add("valid"); 
                            cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS + i].classList.add("placeholder");
                        }                
                    }
                    
                    cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS].innerHTML = FIRSTLETTER;
                    cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS].classList.remove("placeholder");

                    if(cellBeforeFirstEmptyCell.index + 1 - NBLETTERS != 0){
                        cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS].classList.add("valid"); 
                    } else {
                        cells[cellBeforeFirstEmptyCell.index + 1 - NBLETTERS].classList.remove("valid"); 
                    }
                    end = false;
                  }, 300);
                }
            }
        } else {
            console.log(event.key);
        }
    }
});