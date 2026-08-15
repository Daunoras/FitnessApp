class Chart {
    constructor(canvasId, data, model) {
        this.canvas = document.getElementById(canvasId);
        if (this.canvas.getContext) {
            this.ctx = this.canvas.getContext('2d');
        } else {
            console.error('error with canvas');
        }
        this.data = data.data;
        this.model = model;
        this.normalizedDates = [];
        this.coordinates = [];
        this.lines = [];
        window.addEventListener('resize', () => this.resizeChart());
    }

    setLines() {
        for (let i = 0; i < this.data.length; i++) {
            let line = this.setLinePoints(this.data[i]);
            this.lines.push(line);
        }
    }

    setLinePoints(lineData) {
        let linePoints = [];
        for (let i = 0; i < lineData.dates.length; i++) {
            let point = {
                x: undefined,
                y: undefined,
                date: lineData.dates[i],
                value: lineData.data[i],
                info: lineData.info
            }
            linePoints.push(point);
        }
        return linePoints;
    }

    transformDates() {
        this.normalizedDates.length = 0;

        let allTimestamps = [];
        let minDates = [];
        let maxDates = [];

        for (let i = 0; i < this.data.length; i++) {
            let timestamps = this.data[i].dates.map(date => new Date(date).getTime());
            let minDate = Math.min(...timestamps);
            let maxDate = Math.max(...timestamps);
            allTimestamps.push(timestamps);
            minDates.push(minDate);
            maxDates.push(maxDate);
        }

        let startingDate = Math.min(...minDates);
        let dateEndPoint = Math.max(...maxDates) - startingDate;

        for (let i = 0; i < allTimestamps.length; i++) {
            let offsetedDates = allTimestamps[i].map(date => date - startingDate);
            let normalized = offsetedDates.map(date => date / dateEndPoint);
            this.normalizedDates.push(normalized);
        }
    }

    generateCoordinates() {
        this.coordinates.length = 0;
        for (let i = 0; i < this.data.length; i++) {
            let coordinates = this.generateLineCoordinates(i);
            this.coordinates.push(coordinates);
        }
    }

    generateLineCoordinates(index) {
        let maxValue = Math.max(...this.data[index].data);
        let lineCoordinates = [];
        if (this.data[index].data.length == 1 && this.data.length == 1) {
            let x = (this.canvas.width - 100) * 0.5 + 80;
            let y = (this.canvas.height - 50) - 0.7 * (this.canvas.height - 90);
            this.points[0]['x'] = x;
            this.points[0]['y'] = y;
            lineCoordinates.push([x, y]);
        } else {
            for (let i = 0; i < this.data[index].data.length; i++) {
                let x = (this.canvas.width - 100) * this.normalizedDates[index][i] + 80;
                let y = (this.canvas.height - 50) - (this.data[index].data[i] / maxValue) * (this.canvas.height - 90);
                this.lines[index][i]['x'] = x;
                this.lines[index][i]['y'] = y;
                lineCoordinates.push([x, y]);
            }
        }
        lineCoordinates.sort((a, b) => a[0] - b[0]);
        return lineCoordinates;
    }

    getLineColor(index) {
         const hue = (index * 137.508) % 360;
         return `oklch(65% 0.15 ${hue})`;
    }

    drawLineChart() {
        if (!this.ctx || this.coordinates.length == 0) return;
        for (let i = 0; i < this.coordinates.length; i++) {
            this.drawLine(this.coordinates[i], this.getLineColor(i));
        }
    }

    drawLine(coordinates, lineColor) {
        if (coordinates.length == 0) return;
        this.ctx.beginPath();
        this.ctx.moveTo(coordinates[0][0], coordinates[0][1]);

        for (let i = 1; i < coordinates.length; i++){
            this.ctx.lineTo(coordinates[i][0], coordinates[i][1]);
        }
        this.ctx.strokeStyle = lineColor;
        this.ctx.stroke();

        for (let i = 0; i < coordinates.length; i++) {
            this.ctx.beginPath();
            this.ctx.arc(coordinates[i][0], coordinates[i][1], 3, 0, 2 * Math.PI);
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
        this.model = model;
        this.lines = [];
        this.setLines();
        this.transformDates();
        this.generateCoordinates();
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
        this.generateCoordinates();
        this.drawAxis();
        this.drawLineChart();
    }

    initialDraw() {
        this.setLines();
        this.resizeCanvas();
        this.transformDates();
        this.generateCoordinates();
        this.drawAxis();
        this.drawLineChart();
    }

}

export default Chart;