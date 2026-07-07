const PALETTE = {
    primary: "#4f46e5",
    primaryLight: "rgba(79, 70, 229, 0.15)",
    success: "#16a34a",
    successLight: "rgba(22, 163, 74, 0.15)",
    warning: "#d97706",
    danger: "#dc2626",
    grid: "#eceef3",
    text: "#6b7280",
};

Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
Chart.defaults.color = PALETTE.text;
Chart.defaults.borderColor = PALETTE.grid;

async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Failed to fetch ${url}`);
    return res.json();
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

async function renderDatasetCharts() {
    const data = await fetchJSON("/api/dataset-summary");

    // Smoker vs non-smoker
    new Chart(document.getElementById("smokerChart"), {
        type: "bar",
        data: {
            labels: Object.keys(data.avg_charge_by_smoker).map((k) => (k === "yes" ? "Smoker" : "Non-Smoker")),
            datasets: [{
                label: "Avg. Charge ($)",
                data: Object.values(data.avg_charge_by_smoker),
                backgroundColor: [PALETTE.dangerLight || "rgba(220,38,38,0.5)", PALETTE.successLight],
                borderRadius: 8,
            }],
        },
        options: baseBarOptions(),
    });

    // Region
    const regionLabels = Object.keys(data.avg_charge_by_region).map(capitalize);
    new Chart(document.getElementById("regionChart"), {
        type: "doughnut",
        data: {
            labels: regionLabels,
            datasets: [{
                data: Object.values(data.avg_charge_by_region),
                backgroundColor: ["#4f46e5", "#16a34a", "#d97706", "#0891b2"],
                borderWidth: 0,
            }],
        },
        options: {
            plugins: { legend: { position: "bottom" } },
            cutout: "60%",
        },
    });

    // Age group
    new Chart(document.getElementById("ageChart"), {
        type: "line",
        data: {
            labels: Object.keys(data.avg_charge_by_age_group),
            datasets: [{
                label: "Avg. Charge ($)",
                data: Object.values(data.avg_charge_by_age_group),
                borderColor: PALETTE.primary,
                backgroundColor: PALETTE.primaryLight,
                fill: true,
                tension: 0.35,
                pointBackgroundColor: PALETTE.primary,
            }],
        },
        options: baseBarOptions(),
    });

    // BMI vs charges scatter
    const smokerPoints = data.bmi_vs_charge_sample.filter((d) => d.smoker === "yes");
    const nonSmokerPoints = data.bmi_vs_charge_sample.filter((d) => d.smoker === "no");
    new Chart(document.getElementById("bmiChart"), {
        type: "scatter",
        data: {
            datasets: [
                {
                    label: "Smoker",
                    data: smokerPoints.map((d) => ({ x: d.bmi, y: d.charges })),
                    backgroundColor: "rgba(220,38,38,0.6)",
                },
                {
                    label: "Non-Smoker",
                    data: nonSmokerPoints.map((d) => ({ x: d.bmi, y: d.charges })),
                    backgroundColor: "rgba(22,163,74,0.6)",
                },
            ],
        },
        options: {
            plugins: { legend: { position: "bottom" } },
            scales: {
                x: { title: { display: true, text: "BMI" }, grid: { color: PALETTE.grid } },
                y: { title: { display: true, text: "Charges ($)" }, grid: { color: PALETTE.grid } },
            },
        },
    });
}

async function renderModelChart() {
    const scores = await fetchJSON("/api/model-scores");
    const labels = Object.keys(scores);
    const values = Object.values(scores).map((v) => Number(v.toFixed(3)));

    new Chart(document.getElementById("modelChart"), {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "R² Score",
                data: values,
                backgroundColor: labels.map((l) =>
                    l === "Random Forest Regressor" ? PALETTE.primary : "rgba(79,70,229,0.35)"
                ),
                borderRadius: 6,
            }],
        },
        options: {
            indexAxis: "y",
            plugins: { legend: { display: false } },
            scales: {
                x: { min: 0, max: 1, grid: { color: PALETTE.grid } },
                y: { grid: { display: false } },
            },
        },
    });
}

async function renderHistoryChart() {
    const history = await fetchJSON("/api/my-history");

    new Chart(document.getElementById("historyChart"), {
        type: "line",
        data: {
            labels: history.map((h) => h.date),
            datasets: [{
                label: "Predicted Charge ($)",
                data: history.map((h) => h.predicted_charge),
                borderColor: PALETTE.success,
                backgroundColor: PALETTE.successLight,
                fill: true,
                tension: 0.3,
                pointBackgroundColor: PALETTE.success,
            }],
        },
        options: baseBarOptions(),
    });
}

function baseBarOptions() {
    return {
        plugins: { legend: { display: false } },
        scales: {
            x: { grid: { display: false } },
            y: { grid: { color: PALETTE.grid }, beginAtZero: true },
        },
    };
}

document.addEventListener("DOMContentLoaded", () => {
    renderDatasetCharts().catch(console.error);
    renderModelChart().catch(console.error);
    renderHistoryChart().catch(console.error);
});
