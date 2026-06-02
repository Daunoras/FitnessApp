import Chart from './canvas_chart.js';

function fetchDataAndRenderChart(model, startDate, endDate) {

    const url = `/fitness/api/chart/data/?model=${model}&date_from=${startDate}&date_to=${endDate}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (myChart) {
                myChart.updateData(data, model)
            } else {
                myChart = new Chart('myChart', data, model);
                myChart.initialDraw();
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

let myChart = null;
document.addEventListener('DOMContentLoaded', function() {
    const modelSelector = document.getElementById('dataSelector');
    const dateFrom = document.getElementById('date_from');
    const dateTo = document.getElementById('date_to');
    fetchDataAndRenderChart(modelSelector.value, dateFrom.value, dateTo.value);

    modelSelector.addEventListener('change', function() {
         fetchDataAndRenderChart(this.value, dateFrom.value, dateTo.value);
    });

    dateFrom.addEventListener('change', function() {
        fetchDataAndRenderChart(modelSelector.value, this.value, dateTo.value)
    });

    dateTo.addEventListener('change', function() {
        fetchDataAndRenderChart(modelSelector.value, dateFrom.value, this.value)
    });
});