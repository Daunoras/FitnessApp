import Chart from './canvas_chart.js';
import { fetchChartData, loadChart, validateDates } from './chart_service.js';
import { findPoint, tooltipText, showTooltip, hideTooltip } from './tooltip.js';


let nutritionChart = null;
let weightChart = null;

document.addEventListener('DOMContentLoaded', async function() {
    const nutritionCanvas = document.getElementById('nutrition-chart');
    const weightCanvas = document.getElementById('weight-chart');

    nutritionChart = await loadChart('nutrition', '', '', '', nutritionChart, 'nutrition-chart');
    weightChart = await loadChart('weight', '', '', '', weightChart, 'weight-chart');

    nutritionCanvas.addEventListener('mousemove', e => {
        const rect = nutritionCanvas.getBoundingClientRect();
        const point = findPoint(
            e.clientX - rect.left,
            e.clientY - rect.top,
            nutritionChart
        );
        if (point) {
            showTooltip('nutrition', point, e.pageX, e.pageY);
        }
        else {
            hideTooltip();
        }
    });

    weightCanvas.addEventListener('mousemove', e => {
        const rect = weightCanvas.getBoundingClientRect();
        const point = findPoint(
            e.clientX - rect.left,
            e.clientY - rect.top,
            weightChart
        );
        if (point) {
            showTooltip('weight', point, e.pageX, e.pageY);
        }
        else {
            hideTooltip();
        }
    });

});