/** Initialisation */
generateChart = (id, config) => new Chart(document.getElementById(id), config)

Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
Chart.defaults.font.weight = '400';
Chart.defaults.color = '#565656';

/** Manage modals */
function preventScroll(event) {
    event.preventDefault();
}

function disableScroll() {
    document.addEventListener("wheel", preventScroll, { passive: false });
    document.addEventListener("touchmove", preventScroll, { passive: false });
}

function enableScroll() {
    document.removeEventListener("wheel", preventScroll);
    document.removeEventListener("touchmove", preventScroll);
}

document.addEventListener("DOMContentLoaded", function () {
    const openModalBtn = document.querySelectorAll(".modal-btn");
    const modal = document.getElementById("open-modal");
    const closeModalElements = modal.querySelectorAll(".modal-close, .modal-backdrop");
    const modalIframe = document.getElementById("modal-iframe");

    openModalBtn.forEach(btn => btn.addEventListener("click", function () {
        modalIframe.src = "table?" + btn.getAttribute("aria-params");
        modal.classList.add("active");
        disableScroll(); // Bloquer le scroll
    }));

    closeModalElements.forEach(element => {
        element.addEventListener("click", function () {
            modal.classList.remove("active");
            enableScroll(); // Débloquer le scroll
        });
    });
});

/** Manage requests */
requests_elmts = document.querySelectorAll(".request");
promises = Array.from(requests_elmts).map(elmt => new Promise((resolve)  => {
    fetch("fetch?" + elmt.getAttribute("aria-params")).then((res) =>{
        res.text().then(txt  => resolve([txt, elmt]));
    })
}));
Promise.all(promises).then(proms => proms.forEach(prom =>  {
    [txt, elmt] = prom;
    document.getElementById(elmt.getAttribute("aria-txt")).innerHTML = txt;
    elmt.classList.add('hidden');
    document.getElementById(elmt.getAttribute("aria-related")).classList.remove('hidden');
}));

/** Differents charts */

generateChart('chart1', {
    type: 'bar',
    data: {
        labels: ['Rouge', 'Bleu', 'Jaune', 'Vert', 'Violet', 'Orange'],
        datasets: [{
        label: 'Nb de Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        backgroundColor:  '#EC643C'
        }]
    },
    options: {
        scales: {
        y: {
            beginAtZero: true
        }
        },
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
})

generateChart('chart2', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart3', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart4-1', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart4-2', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart4-3', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart4-4', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart5', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart6', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart7-1', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart7-2', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })

  generateChart('chart7-3', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'Mon premier jeu de données',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false // Désactive l'affichage de la légende
            }
        },
        responsive: true,  // Active le redimensionnement automatique
        maintainAspectRatio: false, // Permet d'adapter la hauteur indépendamment de la largeur
    }
  })