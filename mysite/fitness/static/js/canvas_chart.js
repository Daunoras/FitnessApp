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
        this.points = [];
        window.addEventListener('resize', () => this.resizeChart());
    }

    setPoints() {
        for (let i = 0; i < this.data.length; i++) {
            let point = {
                x: undefined,
                y: undefined,
                date: this.labels[i],
                value: this.data[i]
            }
            this.points.push(point);
        }
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
        for (let i = 0; i < this.data.length; i++) {
            let x = (this.canvas.width - 100) * this.normalizedDates[i] + 80;
            let y = (this.canvas.height - 50) - (this.data[i] / maxValue) * (this.canvas.height - 90);
            this.points[i]['x'] = x;
            this.points[i]['y'] = y;
            this.coordinates.push([x, y]);
        }
        console.log(this.points);
        this.coordinates.sort((a, b) => a[0] - b[0]);
    }

    drawLineChart() {
        if (!this.ctx) return;
        this.ctx.beginPath();
        this.ctx.moveTo(this.coordinates[0][0], this.coordinates[0][1]);

        for (let i = 1; i < this.coordinates.length; i++){
            this.ctx.lineTo(this.coordinates[i][0], this.coordinates[i][1]);
        }
        this.ctx.strokeStyle = 'red';
        this.ctx.stroke();

        for (let i = 0; i < this.coordinates.length; i++) {
            this.ctx.beginPath();
            this.ctx.arc(this.coordinates[i][0], this.coordinates[i][1], 3, 0, 2 * Math.PI);
            this.ctx.fill();
        }

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
        this.points = [];
        this.setPoints();
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
        this.setPoints();
        this.resizeCanvas();
        this.dateTransformation();
        this.coordinateGeneration();
        this.drawAxis();
        this.drawLineChart();
    }

}

export default Chart;