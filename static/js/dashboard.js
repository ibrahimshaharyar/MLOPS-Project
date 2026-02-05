// Dashboard JavaScript - Fetch data and render charts using Chart.js

// API Base URL
const API_BASE = '/api/dashboard';

// Chart color schemes
const COLORS = {
    primary: '#6366f1',
    secondary: '#10b981',
    accent: '#f59e0b',
    danger: '#ef4444',
    info: '#3b82f6',
    purple: '#a78bfa',
    pink: '#ec4899',
    teal: '#14b8a6'
};

const CHART_COLORS = [
    COLORS.primary,
    COLORS.secondary,
    COLORS.accent,
    COLORS.info,
    COLORS.purple,
    COLORS.pink,
    COLORS.teal,
    COLORS.danger
];

// Global chart instances
let charts = {};

// Fetch and display summary statistics
async function loadSummaryStats() {
    try {
        const response = await fetch(`${API_BASE}/summary`);
        const data = await response.json();

        document.getElementById('totalStudents').textContent = data.total_students;
        document.getElementById('avgMath').textContent = data.avg_math;
        document.getElementById('avgReading').textContent = data.avg_reading;
        document.getElementById('avgWriting').textContent = data.avg_writing;
    } catch (error) {
        console.error('Error loading summary stats:', error);
    }
}

// Load and render score distributions (multi-line chart)
async function loadDistributions() {
    try {
        const response = await fetch(`${API_BASE}/distributions`);
        const data = await response.json();

        const ctx = document.getElementById('distributionChart').getContext('2d');

        // Prepare bin centers from bin edges
        const mathBins = data.math.bins.slice(0, -1).map((b, i) =>
            (b + data.math.bins[i + 1]) / 2
        );

        charts.distribution = new Chart(ctx, {
            type: 'line',
            data: {
                labels: mathBins.map(b => Math.round(b)),
                datasets: [
                    {
                        label: 'Math Scores',
                        data: data.math.counts,
                        borderColor: COLORS.primary,
                        backgroundColor: COLORS.primary + '20',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Reading Scores',
                        data: data.reading.counts,
                        borderColor: COLORS.secondary,
                        backgroundColor: COLORS.secondary + '20',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Writing Scores',
                        data: data.writing.counts,
                        borderColor: COLORS.accent,
                        backgroundColor: COLORS.accent + '20',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Students'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Score Range'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading distributions:', error);
    }
}

// Create pie chart helper
function createPieChart(canvasId, data, title) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    charts[canvasId] = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: CHART_COLORS,
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: false
                }
            }
        }
    });
}

// Load all pie charts
async function loadPieCharts() {
    try {
        // Gender distribution
        const genderData = await fetch(`${API_BASE}/gender`).then(r => r.json());
        createPieChart('genderChart', genderData, 'Gender Distribution');

        // Race/ethnicity distribution
        const raceData = await fetch(`${API_BASE}/race`).then(r => r.json());
        createPieChart('raceChart', raceData, 'Race/Ethnicity');

        // Lunch distribution
        const lunchData = await fetch(`${API_BASE}/lunch`).then(r => r.json());
        createPieChart('lunchChart', lunchData, 'Lunch Type');

        // Test prep distribution
        const testPrepData = await fetch(`${API_BASE}/test-prep`).then(r => r.json());
        createPieChart('testPrepChart', testPrepData, 'Test Prep Course');
    } catch (error) {
        console.error('Error loading pie charts:', error);
    }
}

// Load scores by gender (grouped bar chart)
async function loadScoresByGender() {
    try {
        const response = await fetch(`${API_BASE}/scores-by-gender`);
        const data = await response.json();

        const ctx = document.getElementById('scoresByGenderChart').getContext('2d');

        // Calculate averages for each gender
        const genders = Object.keys(data.math);
        const mathAvgs = genders.map(g => {
            const scores = data.math[g];
            return scores.reduce((a, b) => a + b, 0) / scores.length;
        });
        const readingAvgs = genders.map(g => {
            const scores = data.reading[g];
            return scores.reduce((a, b) => a + b, 0) / scores.length;
        });
        const writingAvgs = genders.map(g => {
            const scores = data.writing[g];
            return scores.reduce((a, b) => a + b, 0) / scores.length;
        });

        charts.scoresByGender = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: genders.map(g => g.charAt(0).toUpperCase() + g.slice(1)),
                datasets: [
                    {
                        label: 'Math',
                        data: mathAvgs,
                        backgroundColor: COLORS.primary
                    },
                    {
                        label: 'Reading',
                        data: readingAvgs,
                        backgroundColor: COLORS.secondary
                    },
                    {
                        label: 'Writing',
                        data: writingAvgs,
                        backgroundColor: COLORS.accent
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Average Score'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading scores by gender:', error);
    }
}

// Load correlation matrix
async function loadCorrelation() {
    try {
        const response = await fetch(`${API_BASE}/correlation`);
        const data = await response.json();

        const ctx = document.getElementById('correlationChart').getContext('2d');

        // Create heatmap-style matrix using bar chart
        const labels = data.labels.map(l => l.replace('_score', '').replace('_', ' '));

        // Flatten matrix for display
        const correlationData = [];
        data.matrix.forEach((row, i) => {
            row.forEach((val, j) => {
                if (i < j) { // Only upper triangle
                    correlationData.push({
                        x: `${labels[i]} vs ${labels[j]}`,
                        y: val
                    });
                }
            });
        });

        charts.correlation = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: correlationData.map(d => d.x),
                datasets: [{
                    label: 'Correlation Coefficient',
                    data: correlationData.map(d => d.y),
                    backgroundColor: CHART_COLORS[0]
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        min: 0,
                        max: 1,
                        title: {
                            display: true,
                            text: 'Correlation'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading correlation matrix:', error);
    }
}

// Initialize dashboard
async function initDashboard() {
    console.log('Loading dashboard data...');

    await Promise.all([
        loadSummaryStats(),
        loadDistributions(),
        loadPieCharts(),
        loadScoresByGender(),
        loadCorrelation()
    ]);

    console.log('Dashboard loaded successfully!');
}

// Load dashboard when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
} else {
    initDashboard();
}
