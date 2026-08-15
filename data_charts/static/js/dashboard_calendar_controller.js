import ActivityCalendar from "./activity_calendar.js";
import { findPoints, tooltipText, showTooltip, hideTooltip } from './tooltip.js';
import { fetchCalendarData, updatePopover } from './calendar_service.js';


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
    document.getElementById("menu-info").innerHTML =
        `<span>${day.date}</span>
        <br>
        <span>${day.workout_type}</span>
        <br>
        <span>${day.nutritionInfo}</span>
        <br>
        <span>${day.weightInfo}</span>`;
    activityCalendar.selectedDay = day;
    updatePopover(day);
    menu.showPopover();
});