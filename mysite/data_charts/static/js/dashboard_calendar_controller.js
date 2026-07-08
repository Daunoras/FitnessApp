import ActivityCalendar from "./activity_calendar.js";

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



const calendarContainer = document.getElementById("calendar-grid");

let backendCalendarData = await fetchCalendarData();
const activityCalendar = new ActivityCalendar(calendarContainer, backendCalendarData);
activityCalendar.render();