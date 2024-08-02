class Chart {
    constructor(canvasId, data) {
        this.canvas = document.getElementById(canvasId);
        if (this.canvas.getContext) {
            this.ctx = this.canvas.getContext('2d');
        } else {
            console.error('error with canvas')
        }
        this.data = data;
    }

    drawLineChart() {
        if (!this.ctx) return;
        this.ctx.beginPath();
        this.ctx.moveTo(10, this.canvas.height - (this.data[0] / Math.max(...this.data)) * this.canvas.height);

        this.data.forEach((value, index) => {
            let x = 10 + index * (this.canvas.width / this.data.length);
            let y = this.canvas.height - (value / Math.max(...this.data)) * this.canvas.height;
            this.ctx.lineTo(x, y);
        });

        this.ctx.strokeStyle = 'red';
        this.ctx.stroke();
    }

    updateData(newData) {
        this.data = newData;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawLineChart();
    }

}