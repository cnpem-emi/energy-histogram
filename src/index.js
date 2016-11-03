import { Chart, BarController, BarElement, CategoryScale, LinearScale } from 'chart.js';

Chart.register(BarController, BarElement, CategoryScale, LinearScale)

var canvas = document.getElementById("freq-chart");

var chart = new Chart(canvas, {
    type: "bar",
    data: {
        labels: [],
        datasets: [
            {
                label: "Energy Frequency",
                backgroundColor: "rgb(75,192,192)",
                data: []
            }
        ]
    }
});

async function updateChart() {
    const response = await fetch(`http://${window.location.host}/points`);
    const data = await response.json();

    console.log(data.y);

    chart.data.datasets[0].data = data.y;
    chart.data.labels = data.x;

    chart.update();
}

window.onload = async function () {
    updateChart();

    setInterval(updateChart, 5000);
};
