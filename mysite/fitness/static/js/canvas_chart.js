class Chart {
    constructor(canvasId, data, model) {
        this.canvas = document.getElementById(canvasId);
        if (this.canvas.getContext) {
            this.ctx = this.canvas.getContext('2d');
        } else {
            console.error('error with canvas');
        }
        this.data = data.data;
        this.labels = data.labels;
        this.model = model;
        this.normalizedDates = [];
        this.coordinates = [];
        window.addEventListener('resize', () => this.resizeChart());
    }

    dateTransformation() {
        let timestamps = this.labels.map(label => new Date(label).getTime());
        let minDate = Math.min(...timestamps);
        let offsetedDates = timestamps.map(date => date - minDate);
        let dateEndPoint = Math.max(...offsetedDates);
        this.normalizedDates = offsetedDates.map(date => date / dateEndPoint);
    }

    coordinateGeneration() {
        let maxValue = Math.max(...this.data);
        this.coordinates.length = 0;
        this.data.forEach((value, index) => {
            let x = (this.canvas.width - 100) * this.normalizedDates[index] + 80
            let y = (this.canvas.height - 50) - (value / maxValue) * (this.canvas.height - 90);
            this.coordinates.push([x, y]);
        });
        this.coordinates.sort((a, b) => a[0] - b[0]);
    }

    drawLineChart() {
        if (!this.ctx) return;
        this.ctx.beginPath();
        this.ctx.moveTo(this.coordinates[0][0], this.coordinates[0][1]);
        this.coordinates.forEach(coordinate => {
            this.ctx.lineTo(coordinate[0], coordinate[1]);
        });
        this.ctx.strokeStyle = 'red';
        this.ctx.stroke();
    }

    drawAxis() {
        let axisCoordinates = [];
        axisCoordinates.push(
            [70, 40],
            [70, this.canvas.height - 50],
            [this.canvas.width - 20, this.canvas.height - 50]
        );
        this.ctx.beginPath();
        this.ctx.moveTo(axisCoordinates[0][0], axisCoordinates[0][1]);
        axisCoordinates.forEach(coordinate => {
            this.ctx.lineTo(coordinate[0], coordinate[1]);
        });
        this.ctx.strokeStyle = 'gray';
        this.ctx.stroke();
        this.ctx.font = '22px Arial';
        this.ctx.fillStyle = 'black';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(this.model, this.canvas.width / 2, 20);

    }

    updateData(newData, model) {
        this.data = newData.data;
        this.labels = newData.labels;
        this.model = model;
        this.dateTransformation();
        this.coordinateGeneration();
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawAxis();
        this.drawLineChart();
    }

    resizeCanvas() {
        const container = this.canvas.parentElement;
        this.canvas.width = container.clientWidth;
        this.canvas.height = this.canvas.width * 0.6;
    }

    resizeChart() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.resizeCanvas();
        this.coordinateGeneration();
        this.drawAxis();
        this.drawLineChart();
    }

    initialDraw() {
        this.resizeCanvas();
        this.dateTransformation();
        this.coordinateGeneration();
        this.drawAxis();
        this.drawLineChart();
    }

}

export default Chart;