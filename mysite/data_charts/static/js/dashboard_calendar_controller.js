import ActivityCalendar from "./activity_calendar.js";

const calendarContainer = document.getElementById("calendar-grid");
const activityCalendar = new ActivityCalendar(calendarContainer);
activityCalendar.render();