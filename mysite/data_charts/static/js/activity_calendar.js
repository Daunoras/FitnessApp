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
            this.container.appendChild(dayCard);
        }
    }
}

export default ActivityCalendar;