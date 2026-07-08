class ActivityCalendar {
    constructor(container, datesData) {
        this.container = container;
        this.days = datesData;
    }

    render() {
        console.log(this.days);
        for (let day of this.days) {
            let dayCard = document.createElement("div");
            dayCard.textContent = day.date;
            dayCard.className = 'day';
            if (day.is_today == true) {
                dayCard.classList.add('today')
            }
            if (day.is_future == true) {
                dayCard.classList.add('future')
            }
            this.container.appendChild(dayCard);
        }
    }
}

export default ActivityCalendar;