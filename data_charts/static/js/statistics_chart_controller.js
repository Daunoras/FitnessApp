import Chart from './canvas_chart.js';
import { fetchChartData, loadChart, validateDates } from './chart_service.js';
import { findPoint, tooltipText, showTooltip, hideTooltip } from './tooltip.js';


let dataChart = null;
document.addEventListener('DOMContentLoaded', async function() {
    const modelSelector = document.getElementById('dataSelector');
    const dateFrom = document.getElementById('date_from');
    const dateTo = document.getElementById('date_to');
    const lift = document.getElementById('exerciseSelection');
    const canvas = document.getElementById('statisticsDataChart');

    dataChart = await loadChart(modelSelector.value, dateFrom.value, dateTo.value, lift.value, dataChart, 'statisticsDataChart');

    modelSelector.addEventListener('change', function() {
        if (this.value == 'exercise'){
            lift.style.display = 'inline';
        } else {
            lift.style.display = 'none';
        }
        loadChart(this.value, dateFrom.value, dateTo.value, lift.value, dataChart, 'statisticsDataChart');
    });

    dateFrom.addEventListener('change', function() {
        loadChart(modelSelector.value, this.value, dateTo.value, lift.value, dataChart, 'statisticsDataChart')
    });

    dateTo.addEventListener('change', function() {
        loadChart(modelSelector.value, dateFrom.value, this.value, lift.value, dataChart, 'statisticsDataChart')
    });

    lift.addEventListener('change', function() {
        loadChart(modelSelector.value, dateFrom.value, dateTo.value, this.value, dataChart, 'statisticsDataChart')
    });

    canvas.addEventListener('mousemove', e => {
        const rect = canvas.getBoundingClientRect();
        const point = findPoint(
            e.clientX - rect.left,
            e.clientY - rect.top,
            dataChart
        );
        if (point) {
            showTooltip(modelSelector.value, point, e.pageX, e.pageY);
        }
        else {
            hideTooltip();
        }
    });
});