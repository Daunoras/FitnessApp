import ActivityCalendar from "./activity_calendar.js";
import { findPoint, tooltipText, showTooltip, hideTooltip } from './tooltip.js';

async function fetchCalendarData() {

    const url = `/data_charts/api/dashboard/calendar/`;

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


function updatePopover(day) {
    let trainingButton = document.getElementById("training-button");
    if (day.workout_type) {
        trainingButton.textContent = "View workout";
        trainingButton.href = day.viewWorkoutURL;
    } else {
        trainingButton.textContent = "Add workout";
        trainingButton.href = day.addWorkoutURL;
    }
}

const calendarContainer = document.getElementById("calendar-grid");

let backendCalendarData = await fetchCalendarData();
const activityCalendar = new ActivityCalendar(calendarContainer, backendCalendarData);
activityCalendar.render();

calendarContainer.addEventListener("click", (e) => {
    const card = e.target.closest(".day");
    if (!card) {
        menu.hidePopover();
        return;
    }
    const day = activityCalendar.dayData.get(card);
    document.getElementById("menu-info").innerHTML = `<span>${day.date}</span> <br> <span>${day.workout_type}</span>`;
    activityCalendar.selectedDay = day;
    updatePopover(day);
    menu.showPopover();
});