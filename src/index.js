import { Chart, BarController, BarElement, CategoryScale, LinearScale } from "chart.js"
import zoomPlugin from 'chartjs-plugin-zoom';

Chart.register(BarController, BarElement, CategoryScale, LinearScale, zoomPlugin)

var canvas = document.getElementById("freq-chart");

const scaleOpts = {
    grid: {
        color: 'rgba( 0, 0, 0, 0.1)',
    },
};

const scales = {
    x: {
        type: 'category',
        title: {
            display: true,
            text: "Energy Level",
        },
    },
    y: {
        title: {
            display: true,
            text: "# of Occurences",
        },
        type: 'linear',
        ticks: {
            callback: (val, index, ticks) => index === 0 || index === ticks.length - 1 ? null : val,
        },
    },
};
Object.keys(scales).forEach(scale => Object.assign(scales[scale], scaleOpts));

const config = {
    type: 'bar',
    data: {
        labels: [...Array(4096).keys()],
        datasets: [
            {
                label: "Energy Frequency",
                backgroundColor: "rgb(75,192,192)",
                data: []
            }
        ]
    },
    options: {
        scales: scales,
        plugins: {
            tooltip: false,
            zoom: {
                pan: {
                    enabled: true,
                    mode: 'x',
                    modifierKey: 'ctrl',
                },
                zoom: {
                    drag: {
                        enabled: true
                    },
                    mode: 'x',
                },
            }
        },
    }
};

var chart = new Chart(canvas, config);

async function updateChart() {
    const response = await fetch(`http://${window.location.host}:5001/all`);
    const data = await response.json();

    chart.data.datasets[0].data = data;

    chart.update();
}

async function resetReadings() {
    if (!confirm('Are you sure you want to delete ALL readings? This operation cannot be reverted')) return;
    await fetch(`http://${window.location.host}:5001/zero`, { method: "DELETE" });
    updateChart();
}

async function applyCapSleep() {
    // TODO: Filter input
    await fetch(`http://${window.location.host}:5001/cap`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({
            time: parseFloat(document.getElementById("cap-sleep").value),
        }),
    });
    updateChart();
}

window.onload = async function () {
    document.getElementById("reset-zoom").onclick = chart.resetZoom;
    document.getElementById("reset-readings").onclick = resetReadings;
    document.getElementById("apply-cap-sleep").onclick = applyCapSleep;

    const response = await fetch(`http://${window.location.host}:5001/cap`);
    const data = await response.json();

    document.getElementById("cap-sleep").value = data.time;

    updateChart();
    setInterval(updateChart, 5000);
};
