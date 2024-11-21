const confetti = new Confetti();

const style = document.createElement('style');
document.head.appendChild(style);

let NBLETTERS = real_word.length;
const NBTRY = 6;
let FIRSTLETTER = real_word[0];

let dico = [];

let confirmed = false;
let end = false;

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
    res = []

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
    style.innerHTML = `
        :root {
            --outer-margin-top: 8px;
            --outer-margin-bottom: 8px;
            --outer-margin-left: 8px;
            --outer-margin-right: 8px;
            --nb-letters: ${NBLETTERS};
            --nb-try: ${NBTRY};
            --gap: 0.8vmin;
        }
        .grid-container {
            grid-template-columns: repeat(var(--nb-letters), 1fr); /* 7 colonnes égales */
            grid-template-rows: repeat(var(--nb-try), 1fr);   /* 6 lignes égales */
            aspect-ratio: var(--nb-letters) / var(--nb-try); /* Ratio largeur / hauteur */
            inline-size: min(100%, calc((100vh - var(--outer-margin-top) - var(--outer-margin-bottom)) * (var(--nb-letters) / var(--nb-try)))); /* Gère la largeur */
            block-size: min(100%, calc((100vw - var(--outer-margin-left) - var(--outer-margin-right)) * (var(--nb-try) / var(--nb-letters)))); /* Gère la hauteur */
            gap: var(--gap); /* Gap entre deux cellules */
        }
        .cell {
            font-size: calc((min(calc(100vh - var(--outer-margin-top) - var(--outer-margin-bottom)), calc((100vw - var(--outer-margin-left) - var(--outer-margin-right)) * (var(--nb-try) / var(--nb-letters)))) - (var(--nb-try) - 1) * var(--gap)) / var(--nb-try) / 2); /* Taille du texte = hauteur d'une cellule / 2*/
        }
    `;

    // Sélection du conteneur de la grille
    const container = document.querySelector('.grid-container');
  
    // Générer les NBLETTERS x NBTRY cellules
    for (let i = 0; i < NBLETTERS * NBTRY; i++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      if (i === 0) cell.innerHTML = FIRSTLETTER;
      container.appendChild(cell);
    }
  });

document.addEventListener('keydown', function(event) {
    const cells = Array.from(document.querySelectorAll("div.cell"));
    let lastFilledCell = null;
    for (let i = cells.length - 1; i >= 0; i--) {
        if (cells[i].innerHTML !== "") {
            lastFilledCell = { cell: cells[i], index: i };
            break;
        }
    }

    // Vérifier si la touche est une lettre (a-z ou A-Z)
    if(!end){
        if (event.key.length === 1 && /[a-zA-Z]/.test(event.key)) {
            if((lastFilledCell.index + 1) % NBLETTERS !== 0 || confirmed){
                if(lastFilledCell.index % NBLETTERS !== 0 || cells[lastFilledCell.index].innerHTML !== event.key.toUpperCase()){
                    cells[lastFilledCell.index + 1].innerHTML = event.key.toUpperCase();
                    confirmed = false;
                }
            }
        } else if (event.key == "Backspace"){
            if (lastFilledCell && lastFilledCell.index % NBLETTERS !== 0) {
                lastFilledCell.cell.innerHTML = ""; // Efface le contenu
            }
        } else if (event.key == "Enter"){
            if ((lastFilledCell.index + 1) % NBLETTERS === 0) {
                const word = cells.slice(lastFilledCell.index + 1 - NBLETTERS, lastFilledCell.index + 1).map(cell => cell.innerHTML).join("");
                if(dico.includes(word.toLowerCase())){
                  res = verify(word);
                  for(let i = 0; i < res.length; i++){
                      cells[lastFilledCell.index + 1 - NBLETTERS + i].classList.add(res[i] === 2 ? "valid" : (res[i] === 1 ? "good" : "unvalid"));
                  }
      
                  confirmed = true;
                  if(res.every(e => e === 2)){
                      end = true;
                      confetti.launch();
                  } else {
                      cells[lastFilledCell.index + 1].innerHTML = FIRSTLETTER;
                  }
                } else {
                  cells.slice(lastFilledCell.index + 1 - NBLETTERS, lastFilledCell.index + 1).forEach(elmt => elmt.classList.add("uncorrect"));
                  end = true;
                  setTimeout(function(){
                    cells.slice(lastFilledCell.index + 1 - NBLETTERS, lastFilledCell.index + 1).forEach(elmt => {
                      elmt.innerHTML = "";
                      elmt.classList.remove("uncorrect")
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