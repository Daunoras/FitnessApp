class ActivityCalendar {
    constructor(container, datesData) {
        this.container = container;
        this.days = datesData;
        this.dayData = new WeakMap();
        this.selectedDay;
    }

    render() {
        for (let day of this.days) {
            let dayCard = document.createElement("div");
            dayCard.innerHTML = `<span>${day.date}</span><br><span>${day.workout_type}</span>`;
            dayCard.className = 'day';
            dayCard.classList.add(`${day.date}`)
            if (day.is_today == true) {
                dayCard.classList.add('today')
            }
            if (day.is_future == true) {
                dayCard.classList.add('future')
            }
            this.container.appendChild(dayCard);
            this.dayData.set(dayCard, day);
        }
    }
}

export default ActivityCalendar;