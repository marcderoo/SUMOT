generateChart = (id, config) => new Chart(document.getElementById(id), config)

generateChart('chart1', {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
        label: '# of Votes',
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
        }
    }
})

generateChart('chart2', {
    type: 'line',
    data: {
        labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet"],
        datasets: [{
          label: 'My First Dataset',
          data: [65, 59, 80, 81, 56, 55, 40],
          fill: false,
          borderColor: '#EC643C',
          tension: 0.1
        }]
      },
  })