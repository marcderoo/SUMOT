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
        { label: "min", plural: "min", value: 60 },
        { label: "sec", plural: "sec", value: 1 }
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
    const params = elmt.getAttribute("aria-params").replace("__DATEYEAR", new Date(new Date().getFullYear(), 0, 1).toISOString());
    const url = new URL("fetch?" + params, window.location.origin).href;
    acc[url] = {
        callback: (urls) => {
            if (urls[url].json) {
                let res = urls[url].json[0]["_id"];
                if (elmt.hasAttribute("aria-func")) {
                    const func = elmt.getAttribute("aria-func");
                    res = eval(func + "(" + res +")");
                }
                if (elmt.hasAttribute("aria-desc")) {
                    document.getElementById(elmt.getAttribute("aria-desc")).innerHTML = "En " + new Date().getFullYear();
                }
                document.getElementById(elmt.getAttribute("aria-txt")).innerHTML = res;
            }
        }
    };
    return acc;
}, {});

/** Differents charts */
const url_chart1 = new URL('fetch?collection=logs&aggs=[{"$match":{"timestamp":{"$gte":"' + new Date(new Date() - 7 * 24 * 60 * 60 * 1000).toISOString() + '"}}},{"$group":{"_id":{"day":{"$dateToString":{"format":"%Y-%m-%d","date":"$timestamp"}},"ip":"$ip"}}},{"$group":{"_id":"$_id.day","uniqueUsers":{"$sum":1}}},{"$sort":{"_id":1}}]', window.location.origin).href;
urls[url_chart1] = {
    callback: (urls) => {
        if (urls[url_chart1].json) {
            let today = new Date();

            // Tableau pour stocker les jours de la semaine et leurs dates
            let daysOfWeek = [];

            // Remplir le tableau avec les jours (7 jours avant)
            for (let i = 6; i >= 0; i--) {
                let day = new Date(today);
                day.setDate(today.getDate() - i); // Soustrait i jours à la date actuelle
                daysOfWeek.push({
                    day: day.toLocaleString('fr-FR', { weekday: 'long' }), // Nom du jour
                    date: day.toLocaleDateString('fr-FR'), // Date au format JJ/MM/AAAA,
                    dateISO: day.toISOString().split('T')[0] // Date au format ISO (YYYY-MM-DD)
                });
            }

            const months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
            document.getElementById("chart1-desc").innerHTML =  "Du " + daysOfWeek[0].date.split("/")[0] + " " + months[parseInt(daysOfWeek[0].date.split("/")[1]) - 1] + " au " + daysOfWeek[6].date.split("/")[0] + " " + months[parseInt(daysOfWeek[6].date.split("/")[1]) - 1] + " " + daysOfWeek[6].date.split("/")[2];

            generateChart('chart1', {
                type: 'line',
                data: {
                    labels: daysOfWeek.map(d => d.date),
                    datasets: [{
                        label: 'Utilisateurs par jour',
                        data: daysOfWeek.map(d => {
                            const dayData = urls[url_chart1].json.find(item => item._id === d.dateISO);
                            return dayData ? dayData.uniqueUsers : 0;
                        }),
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
        }
    }
};

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

const url_chart4 = new URL('fetch?collection=logs&aggs=[{"$match":{"mode":"ai"}},{"$group":{"_id":{"difficulty":"$difficulty","success":"$success"},"count":{"$sum":1}}},{"$group":{"_id":"$_id.difficulty","total":{"$sum":"$count"},"wins":{"$sum":{"$cond":[{"$eq":["$_id.success",true]},"$count",0]}},"losses":{"$sum":{"$cond":[{"$eq":["$_id.success",false]},"$count",0]}}}},{"$project":{"_id":0,"difficulty":"$_id","winRate":{"$round":[{"$multiply":[{"$divide":["$wins","$total"]},100]},1]},"lossRate":{"$round":[{"$multiply":[{"$divide":["$losses","$total"]},100]},1]},"totalGames":"$total"}},{"$sort":{"difficulty":1}}]', window.location.origin).href;
urls[url_chart4] = {
    callback: (urls) => {
        if (urls[url_chart4].json) {
            const data = urls[url_chart4].json.map((d) => {
                return {
                    difficulty: d.difficulty,
                    winRate: d.winRate,
                    lossRate: d.lossRate
                };
            });
            const charts = ["chart4-1", "chart4-2", "chart4-3", "chart4-4"];
            const difficulties = ["Facile", "Moyen", "Difficile", "Expert"];
            for (let i = 0; i < 4; i++) {
                vals = data.filter((d) => d.difficulty === i).map((d) => [d.winRate, d.lossRate]);
                vals = vals[0] ? vals[0] : [0, 0];
                generateChart(charts[i], {
                    type: 'pie',
                    data: {
                        labels: ["Victoire", "Défaite"],
                        datasets: [{
                            data: vals,
                            backgroundColor: ["#4CAF50", "#EC643C"]
                        }]
                    },
                    options: {
                        plugins: {
                            title: {
                                display: true,
                                text: difficulties[i],
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
            }
        }
    }
};

const url_chart5 = new URL('fetch?collection=logs&aggs=[{"$match":{"mode":"solo"}},{"$project":{"time":1,"bin":{"$switch":{"branches":[{"case":{"$lt":["$time",30000]},"then":"< 30 sec"},{"case":{"$lt":["$time",60000]},"then":"30-60 sec"},{"case":{"$lt":["$time",120000]},"then":"1-2 min"},{"case":{"$lt":["$time",240000]},"then":"2-4 min"},{"case":{"$gt":["$time",300000]},"then":"> 5 min"}],"default":"4-5 min"}}}},{"$group":{"_id":"$bin","count":{"$sum":1}}},{"$sort":{"_id":1}}]', window.location.origin).href;
urls[url_chart5] = {
    callback: (urls) => {
        if (urls[url_chart5].json) {
            let data = urls[url_chart5].json.map((d) => {
                return {
                    bin: d._id,
                    count: d.count
                };
            });

            data = data.sort((a, b) => {
                const order = ["< 30 sec", "30-60 sec", "1-2 min", "2-4 min", "4-5 min", "> 5 min"];
                return order.indexOf(a.bin) - order.indexOf(b.bin);
            });

            const labels = data.map((d) => d.bin);
            const counts = data.map((d) => d.count);
            generateChart('chart5', {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Nombre de parties",
                        data: counts,
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
        }
    }
};

const url_chart6 = new URL('fetch?collection=logs&aggs=[{"$group":{"_id":"$mode","count":{"$sum":1}}},{"$project":{"_id":0,"mode":"$_id","count":1}}]', window.location.origin).href;
urls[url_chart6] = {
    callback: (urls) => {
        if (urls[url_chart6].json) {
            let data = urls[url_chart6].json.map((d) => {
                return {
                    mode: d.mode,
                    count: d.count
                };
            });

            const labels = ["Solo", "IA", "Mot du jour"]
            let counts =[];
            for (let i = 0; i < labels.length; i++) {
                const mode = data.find((d) => d.mode === ["solo", "ai", "daily"][i].toLowerCase());
                counts.push(mode ? mode.count : 0);
            }

            counts = counts.map((d) => d / counts.reduce((a, b) => a + b, 0) * 100);

            generateChart('chart6', {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: counts,
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
        }
    }
};




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