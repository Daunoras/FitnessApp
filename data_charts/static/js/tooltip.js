import Chart from './canvas_chart.js';


function findPoint(mouseX, mouseY, chart) {
    for (const point of chart.points) {
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


export { findPoint, tooltipText, showTooltip, hideTooltip };