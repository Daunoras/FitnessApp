class ActivityCalendar {
    constructor(container) {
        this.container = container;
        this.days = this.generateDates();
    }

    generateDates() {
        const start = new Date();
        start.setDate(start.getDate() - 30);
        start.setDate(start.getDate() - start.getDay() + 1);

        const end = new Date();
        if (end.getDay() != 0) {
            end.setDate(end.getDate() + 7 - end.getDay());
        }

        const days = [];
        const current = new Date(start);

        while (current <= end) {
            days.push(new Date(current));
            current.setDate(current.getDate() + 1);
        }
        return days;
    }

    render() {
        for (let day in this.days) {
            let dayCard = document.createElement("div");
            dayCard.textContent = day;
            this.container.appendChild(dayCard);
        }
    }
}

export default ActivityCalendar;