import Chart from './canvas_chart.js';

function fetchDataAndRenderChart(model, startDate, endDate, lift) {
    if (validateDates(startDate, endDate)) {
    const url = `/data_charts/api/chart/data/?model=${model}&date_from=${startDate}&date_to=${endDate}&lift=${lift}`;
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

function findPoint(mouseX, mouseY) {

    for (const point of myChart.points) {

        const dx = mouseX - point.x;
        const dy = mouseY - point.y;

        const distance = Math.sqrt(dx*dx + dy*dy);

        if (distance < 8) {
            return point;
        }
    }

    return null;
}

function tooltipText(model, point) {
    let text = '';
    if (model == 'nutrition') {
        text = `${point.date}<br>
                Calories: ${point.value}`;
    } else if (model == 'weight') {
        text = `${point.date}<br>
                Bodyweight: ${point.value}`;
    } else if (model == 'exercise') {
        let maxStrength = (((point.value % 1)) < 0.1)? point.value.toFixed(0) : point.value.toFixed(1);
        text = `${point.date}<br>
               Estimated MAX ${maxStrength} kg`;
    }

    return text;
}

function showTooltip(model, point, pageX, pageY) {

    tooltip.innerHTML = tooltipText(model, point);

    tooltip.style.display = "block";

    const offset = 10;

    let left = pageX + offset;
    let top = pageY + offset;

    if (left + tooltip.offsetWidth > window.innerWidth) {
        left = pageX - tooltip.offsetWidth - offset;
    }
    if (top + tooltip.offsetHeight > window.innerHeight) {
        top = pageY - tooltip.offsetHeight - offset;
    }

    tooltip.style.left = left + "px";
    tooltip.style.top = top + "px";
}

function hideTooltip() {
    tooltip.style.display = "none";
}

let myChart = null;
document.addEventListener('DOMContentLoaded', function() {
    const modelSelector = document.getElementById('dataSelector');
    const dateFrom = document.getElementById('date_from');
    const dateTo = document.getElementById('date_to');
    const lift = document.getElementById('exerciseSelection');
    const canvas = document.getElementById('myChart');

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

    canvas.addEventListener('mousemove', e => {
        const rect = canvas.getBoundingClientRect();
        const point = findPoint(
            e.clientX - rect.left,
            e.clientY - rect.top
        );
        if (point) {
            showTooltip(modelSelector.value, point, e.pageX, e.pageY);
        }
        else {
            hideTooltip();
        }
    });
});