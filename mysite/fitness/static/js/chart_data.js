import Chart from './canvas_chart.js';

function fetchDataAndRenderChart(model) {
    const url = `/fitness/api/chart/data/?model=${model}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (myChart) {
                myChart.updateData(data)
            } else {
                myChart = new Chart('myChart', data);
                myChart.drawLineChart();
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

let myChart = null;
document.addEventListener('DOMContentLoaded', function() {
    const selector = document.getElementById('dataSelector');
    fetchDataAndRenderChart(selector.value);

    selector.addEventListener('change', function() {
        fetchDataAndRenderChart(this.value);
    });
});