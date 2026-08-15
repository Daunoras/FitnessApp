import Chart from './canvas_chart.js';


function findPoints(mouseX, mouseY, chart) {
    let points = [];
    for (let i = 0; i < chart.lines.length; i++) {
        for (let j = 0; j < chart.lines[i].length; j++) {
            const dx = mouseX - chart.lines[i][j].x;
            const dy = mouseY - chart.lines[i][j].y;
            const distance = Math.sqrt(dx*dx + dy*dy);

            if (distance < 8) {
                points.push(chart.lines[i][j]);
            }
        }
    }
    return points;
}


function tooltipText(model, points) {
    let text = '';
    for (const point of points) {
        if (model == 'nutrition') {
            if (text == '') {
                text += `${point.date}<br>
                         ${point.info}: ${point.value}`;
            } else {
                text += `<br>${point.info}: ${point.value}`;
            };
        } else if (model == 'weight') {
            text += `${point.date}<br>
                     ${point.info}: ${point.value}`;
        } else if (model == 'exercise') {
            let maxStrength = (((point.value % 1)) < 0.1)? point.value.toFixed(0) : point.value.toFixed(1);
            text += `${point.date}<br>
                     ${point.info}<br>
                     Estimated MAX ${maxStrength} kg`;
        }
    }
    return text;
}


function showTooltip(model, points, pageX, pageY) {
    tooltip.innerHTML = tooltipText(model, points);
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


export { findPoints, tooltipText, showTooltip, hideTooltip };