import Chart from './canvas_chart.js';

function fetchDataAndRenderChart(model, startDate, endDate, lift) {
    if (validateDates(startDate, endDate)) {
    const url = `/fitness/api/chart/data/?model=${model}&date_from=${startDate}&date_to=${endDate}&lift=${lift}`;
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
    } else {
        return;
    }
}

function validateDates(startDate, endDate) {
    const warning = document.getElementById('warning');

    if (startDate && endDate && startDate > endDate) {
        warning.textContent = 'Invalid dates';
        warning.style.display = "block";
        return false;
    }
    warning.style.display = "none";
    return true;
}

let myChart = null;
document.addEventListener('DOMContentLoaded', function() {
    const modelSelector = document.getElementById('dataSelector');
    const dateFrom = document.getElementById('date_from');
    const dateTo = document.getElementById('date_to');
    const lift = document.getElementById('exerciseSelection');
    fetchDataAndRenderChart(modelSelector.value, dateFrom.value, dateTo.value, lift.value);

    modelSelector.addEventListener('change', function() {
        if (this.value == 'exercise'){
            lift.style.display = 'inline';
        } else {
            lift.style.display = 'none';
        }
        fetchDataAndRenderChart(this.value, dateFrom.value, dateTo.value, lift.value);
    });

    dateFrom.addEventListener('change', function() {
        fetchDataAndRenderChart(modelSelector.value, this.value, dateTo.value, lift.value)
    });

    dateTo.addEventListener('change', function() {
        fetchDataAndRenderChart(modelSelector.value, dateFrom.value, this.value, lift.value)
    });

    lift.addEventListener('change', function() {
        fetchDataAndRenderChart(modelSelector.value, dateFrom.value, dateTo.value, this.value)
    });
});