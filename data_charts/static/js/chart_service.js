import Chart from './canvas_chart.js';

async function fetchChartData(model, startDate, endDate, lift) {
    if (!validateDates(startDate, endDate)) {
        return null;
    }
    const url = `/data_charts/api/chart/data/?model=${model}&date_from=${startDate}&date_to=${endDate}&lift=${lift}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching chart data:", error);
        return null;
    }
}


async function loadChart(model, dateFrom, dateTo, lift, chart, canvasId) {
    const data = await fetchChartData(model, dateFrom, dateTo, lift);
    if (!data) return;

    if (chart) {
        chart.updateData(data, model);
    } else {
        chart = new Chart(canvasId, data, model);
        chart.initialDraw();
    }
    return chart;
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

export { fetchChartData, loadChart, validateDates };