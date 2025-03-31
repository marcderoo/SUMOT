/** Initialisation */
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
function multipleFetch(urls) {
    const promises = Object.keys(urls).map(key => new Promise((resolve)  => {
        fetch(key).then((res) => {
            res.json().then((json) => {
                urls[key]["json"] = json;
                resolve();
            });
        });
    }));
    return Promise.all(promises).then(() => {
        Object.keys(urls).forEach(key => {
            if (urls[key].callback) {
                urls[key].callback(urls);
            }
        });
    });
}

function generateChart(id, config, request){
    /*
    const url = new URL("fetch?" + request, window.location.origin).href;
    urls[url] = {
        callback: (urls) => {
            if (urls[url].res) {
                new Chart(document.getElementById(id), config(url));
            }
        }
    };
    */
    return new Chart(document.getElementById(id), config);
}

function disableSkeleton() {
    const skeletons = document.querySelectorAll(".skeleton");
    skeletons.forEach(skeleton => {
        skeleton.remove();
    });
}

function formatTimespan(milliseconds) {
    const seconds = Math.floor(parseFloat(milliseconds / 1000));
    const units = [
        { label: "h", plural: "h", value: 3600 },
        { label: "m", plural: "m", value: 60 },
        { label: "s", plural: "s", value: 1 }
    ];
    
    let remainingSeconds = seconds;
    let result = [];

    for (let { label, plural, value } of units) {
        const count = Math.floor(remainingSeconds / value);
        remainingSeconds %= value;
        if (count > 0) {
            result.push(`${count} ${count > 1 ? plural : label}`);
        }
    }

    return result.join(" ") || "0 s";
}

requests_elmts = document.querySelectorAll(".request");
const urls = Array.from(requests_elmts).reduce((acc, elmt) => {
    const url = new URL("fetch?" + elmt.getAttribute("aria-params"), window.location.origin).href;
    acc[url] = {
        callback: (urls) => {
            if (urls[url].json) {
                let res = urls[url].json[0]["_id"];
                if (elmt.hasAttribute("aria-func")) {
                    const func = elmt.getAttribute("aria-func");
                    res = eval(func + "(" + res +")");
                }
                document.getElementById(elmt.getAttribute("aria-txt")).innerHTML = res;
            }
        }
    };
    return acc;
}, {});

/** Differents charts */
const chart1 = generateChart('chart1', {
    type: 'line',
    data: {
        labels: ['18/03', '19/03', '20/03', '21/03', '22/03', '23/03', '24/03'],
        datasets: [{
            label: 'Utilisateurs par jour',
            data: [12, 13, 15, 14, 16, 17, 19],
            fill: false,
            borderColor: '#EC643C',
            tension: 0.2
        }]
    },
    options: {
        plugins: {
            title: {
                display: false
            },
            subtitle: {
                display: false
            },
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Nombre d’utilisateurs'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
})



/** Chart 2 - Carte du monde avec utilisateurs */
const idToISO3 = {
    250: 'FRA',
    840: 'USA',
    76:  'BRA',
    156: 'CHN',
    356: 'IND',
    276: 'DEU',
    643: 'RUS',
    124: 'CAN',
    36:  'AUS',
    710: 'ZAF'
  };

  const utilisateurs = {
    'FRA': 250,
    'USA': 800,
    'BRA': 420,
    'CHN': 600,
    'IND': 550,
    'DEU': 300,
    'RUS': 320,
    'CAN': 150,
    'AUS': 180,
    'ZAF': 90
  };
  
  
  fetch(new URL("static/libs/countries-50m.json", window.location.origin).href)
  .then((response) => response.json())
  .then((data) => {
    const countries = ChartGeo.topojson.feature(data, data.objects.countries).features;

    const chart2 = generateChart('chart2', {
      type: 'choropleth',
      data: {
        labels: countries.map(d => d.properties.name),
        datasets: [{
          label: 'Utilisateurs par pays',
          data: countries.map(d => {
            const iso = idToISO3[d.id];
            return {
              feature: d,
              value: utilisateurs[iso] || 0
            };
          })
        }]
      },
      options: {
        showOutline: true,
        showGraticule: false,
        scales: {
          projection: {
            axis: 'x',
            projection: 'equalEarth'
          },
          color: {
            axis: 'color',
            quantize: 5,
            legend: {
              position: 'bottom-right',
              title: 'Nombre d’utilisateurs'
            }
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: ctx =>
                `${ctx.chart.data.labels[ctx.dataIndex]} : ${ctx.raw.value} utilisateurs`
            }
          },
          title: {
            display: false
          }
        },
        responsive: true,
        maintainAspectRatio: false
      }
    });
  });

const chart4_1 =  generateChart('chart4-1', {
    type: 'pie',
    data: {
        labels: ["Victoire", "Défaite"],
        datasets: [{
            data: [75, 25],
            backgroundColor: ["#4CAF50", "#EC643C"]
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: "Facile",
                font: {
                    size: 16
                },
                padding: {
                    bottom: 10
                }
            },
            legend: {
                display: true,
                position: 'bottom'
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return `${context.label} : ${context.parsed}%`;
                    }
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
});

const chart4_2 = generateChart('chart4-2', {
    type: 'pie',
    data: {
        labels: ["Victoire", "Défaite"],
        datasets: [{
            data: [55, 45],
            backgroundColor: ["#4CAF50", "#EC643C"]
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: "Moyen",
                font: {
                    size: 16
                },
                padding: {
                    bottom: 10
                }
            },
            legend: {
                display: true,
                position: 'bottom'
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return `${context.label} : ${context.parsed}%`;
                    }
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
});

const chart4_3 = generateChart('chart4-3', {
    type: 'pie',
    data: {
        labels: ["Victoire", "Défaite"],
        datasets: [{
            data: [35, 65],
            backgroundColor: ["#4CAF50", "#EC643C"]
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: "Difficile",
                font: {
                    size: 16
                },
                padding: {
                    bottom: 10
                }
            },
            legend: {
                display: true,
                position: 'bottom'
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return `${context.label} : ${context.parsed}%`;
                    }
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
});

const chart4_4 = generateChart('chart4-4', {
    type: 'pie',
    data: {
        labels: ["Victoire", "Défaite"],
        datasets: [{
            data: [5, 95],
            backgroundColor: ["#4CAF50", "#EC643C"]
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: "Expert",
                font: {
                    size: 16
                },
                padding: {
                    bottom: 10
                }
            },
            legend: {
                display: true,
                position: 'bottom'
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return `${context.label} : ${context.parsed}%`;
                    }
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
});

const chart5 = generateChart('chart5', {
    type: 'bar',
    data: {
        labels: ["May"],
        datasets: [{
            label: "Nombre de joueurs",
            data: [5],
            backgroundColor: '#EC643C'
        }]
    },
    options: {
        plugins: {
            title: {
                display: false
            },
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: "Nombre de joueurs"
                }
            },
            x: {
                title: {
                    display: true,
                    text: "Temps écoulé"
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
  });

const chart6 = generateChart('chart6', {
    type: 'pie',
    data: {
        labels: ["Solo", "IA", "Mot du jour"],
        datasets: [{
            data: [20,50,30],
            backgroundColor: ["#BA68C8", "#FFB74D", "#4FC3F7"]
        }]
    },
    options: {
        plugins: {
            title: {
                display: false
            },
            legend: {
                display: true,
                position: 'bottom'
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return `${context.label} : ${context.parsed}%`;
                    }
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
});




const chart7_1 = generateChart('chart7-1', {
    type: 'line',
    data: {
        labels: ['18/03', '19/03', '20/03', '21/03', '22/03', '23/03', '24/03'],
        datasets: [{
            label: 'Utilisateurs par jour',
            data: [1, 3, 5, 4, 6, 3, 9],
            fill: false,
            borderColor: '#EC643C',
            tension: 0.2
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Solo',
                font: {
                    size: 16
                },
                padding: {
                    top: 10,
                    bottom: 5
                }
            },
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'utilisateurs'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
})




const chart7_2 = generateChart('chart7-2', {
    type: 'line',
    data: {
        labels: ['18/03', '19/03', '20/03', '21/03', '22/03', '23/03', '24/03'],
        datasets: [{
            label: 'Utilisateurs par jour',
            data: [5, 13, 15, 14, 16, 17, 3],
            fill: false,
            borderColor: '#EC643C',
            tension: 0.2
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Mot du jour',
                font: {
                    size: 16
                },
                padding: {
                    top: 10,
                    bottom: 5
                }
            },
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'utilisateurs'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
})




const chart7_3 = generateChart('chart7-3', {
    type: 'line',
    data: {
        labels: ['18/03', '19/03', '20/03', '21/03', '22/03', '23/03', '24/03'],
        datasets: [{
            label: 'Utilisateurs par jour',
            data: [2, 3, 5, 4, 6, 7, 9],
            fill: false,
            borderColor: '#EC643C',
            tension: 0.2
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'IA',
                font: {
                    size: 16
                },
                padding: {
                    top: 10,
                    bottom: 5
                }
            },
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'utilisateurs'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
})

multipleFetch(urls).then(() => {    
    disableSkeleton();
});