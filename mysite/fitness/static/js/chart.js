let myChart = null;

function fetchDataAndRenderChart(model) {
    const url = `/fitness/api/chart/data/?model=${model}`;
    console.log(`Fetching data from: ${url}`);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (myChart) {
                myChart.destroy();
            }

            var ctx = document.getElementById('myChart').getContext('2d');
            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: '${model.charAt(0).toUpperCase() + model.slice(1)} Data',
                        data: data.data,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    const selector = document.getElementById('dataSelector');
    fetchDataAndRenderChart(selector.value);

    selector.addEventListener('change', function() {
        fetchDataAndRenderChart(this.value);
    });
});