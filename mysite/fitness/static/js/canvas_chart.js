class Chart {
    constructor(canvasId, data) {
        this.canvas = document.getElementById(canvasId);
        if (this.canvas.getContext) {
            this.ctx = this.canvas.getContext('2d');
        } else {
            console.error('error with canvas');
        }
        this.data = data.data;
        this.labels = data.labels;
        window.addEventListener('resize', () => this.resize());
    }

    drawLineChart() {
        if (!this.ctx) return;
//          date transformation
        let timestamps = this.labels.map(label => new Date(label).getTime());
        let minDate = Math.min(...timestamps);
        let offsetedDates = timestamps.map(date => date - minDate);
        let dateEndPoint = Math.max(...offsetedDates);
        let normalizedDates = offsetedDates.map(date => date / dateEndPoint);
//          coordinate generation
        let coordinates = [];
        this.data.forEach((value, index) => {
            let x = this.canvas.width * normalizedDates[index]
            let y = this.canvas.height - (value / Math.max(...this.data)) * this.canvas.height;
            coordinates.push([x, y]);
        });
        coordinates.sort((a, b) => a[0] - b[0]);
//          drawing the line
        this.ctx.beginPath();
        this.ctx.moveTo(coordinates[0][0], coordinates[0][1]);
        coordinates.forEach(coordinate => {
            this.ctx.lineTo(coordinate[0], coordinate[1]);
        });
        this.ctx.strokeStyle = 'red';
        this.ctx.stroke();
    }

    updateData(newData) {
        this.data = newData.data;
        this.labels = newData.labels;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawLineChart();
    }

    resize() {
        const container = this.canvas.parentElement;
        this.canvas.width = container.clientWidth;
        this.canvas.height = container.clientHeight;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

}

export default Chart;