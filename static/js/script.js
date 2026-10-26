/* College Event Management System JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto-dismiss Flash Alerts after 5 seconds
    const alertList = document.querySelectorAll('.alert-dismissible');
    alertList.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // 2. Client-side Realtime Table Search Filter Helper
    const tableSearchInputs = document.querySelectorAll('[data-table-search]');
    tableSearchInputs.forEach(input => {
        input.addEventListener('keyup', function () {
            const targetTableId = this.getAttribute('data-table-search');
            const targetTable = document.getElementById(targetTableId);
            if (!targetTable) return;

            const filterValue = this.value.toLowerCase().strip ? this.value.toLowerCase().strip() : this.value.toLowerCase();
            const rows = targetTable.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(filterValue)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // 3. Theme Toggle (Dark / Light Mode)
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        if (theme === 'light') {
            if (themeIcon) {
                themeIcon.className = 'bi bi-sun-fill text-warning';
            }
            if (themeText) {
                themeText.textContent = 'Light';
            }
        } else {
            if (themeIcon) {
                themeIcon.className = 'bi bi-moon-stars-fill text-info';
            }
            if (themeText) {
                themeText.textContent = 'Dark';
            }
        }

        // Live chart updates if on admin dashboard
        if (typeof Chart !== 'undefined') {
            const isLight = (theme === 'light');
            Chart.defaults.color = isLight ? '#64748B' : '#CBD5E1';
            Chart.defaults.borderColor = isLight ? '#E2E8F0' : '#303A52';

            ['categoryChart', 'eventChart', 'trendChart'].forEach(chartId => {
                const chartInstance = Chart.getChart(chartId);
                if (chartInstance) {
                    if (chartInstance.options.scales) {
                        if (chartInstance.options.scales.x) {
                            chartInstance.options.scales.x.grid.color = isLight ? '#E2E8F0' : '#303A52';
                            chartInstance.options.scales.x.ticks.color = isLight ? '#64748B' : '#CBD5E1';
                        }
                        if (chartInstance.options.scales.y) {
                            chartInstance.options.scales.y.grid.color = isLight ? '#E2E8F0' : '#303A52';
                            chartInstance.options.scales.y.ticks.color = isLight ? '#64748B' : '#CBD5E1';
                        }
                    }
                    if (chartInstance.options.plugins && chartInstance.options.plugins.legend) {
                        if (chartInstance.options.plugins.legend.labels) {
                            chartInstance.options.plugins.legend.labels.color = isLight ? '#0F172A' : '#CBD5E1';
                        }
                    }
                    chartInstance.update();
                }
            });
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function () {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(nextTheme);
        });
    }

    // Initialize button state on load
    const activeTheme = document.documentElement.getAttribute('data-theme') || localStorage.getItem('theme') || 'dark';
    applyTheme(activeTheme);
});

/**
 * Utility to render Chart.js charts on Admin Dashboard with Dark Theme Tokens
 */
function renderAdminCharts(categoryLabels, categoryData, eventLabels, eventData, monthlyLabels, monthlyData) {
    if (typeof Chart === 'undefined') return;

    // Global chart defaults for dark mode
    Chart.defaults.color = '#CBD5E1';
    Chart.defaults.borderColor = '#303A52';

    // 1. Events by Category (Doughnut Chart)
    const categoryCtx = document.getElementById('categoryChart');
    if (categoryCtx) {
        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: categoryLabels,
                datasets: [{
                    data: categoryData,
                    backgroundColor: [
                        '#8B5CF6', '#A78BFA', '#15803D', '#1D4ED8',
                        '#92400E', '#B91C1C', '#06B6D4', '#EC4899'
                    ],
                    borderWidth: 2,
                    borderColor: '#151C30'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#CBD5E1' }
                    }
                }
            }
        });
    }

    // 2. Top Events by Registrations (Bar Chart)
    const eventCtx = document.getElementById('eventChart');
    if (eventCtx) {
        new Chart(eventCtx, {
            type: 'bar',
            data: {
                labels: eventLabels,
                datasets: [{
                    label: 'Registrations',
                    data: eventData,
                    backgroundColor: 'rgba(139, 92, 246, 0.85)',
                    borderColor: '#8B5CF6',
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        grid: { color: '#303A52' },
                        ticks: { color: '#CBD5E1' }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0, color: '#CBD5E1' },
                        grid: { color: '#303A52' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // 3. Monthly Registration Trend (Line Chart)
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: 'Registrations Growth',
                    data: monthlyData,
                    borderColor: '#A78BFA',
                    backgroundColor: 'rgba(139, 92, 246, 0.15)',
                    fill: true,
                    tension: 0.35,
                    pointRadius: 4,
                    pointBackgroundColor: '#8B5CF6',
                    pointBorderColor: '#A78BFA'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        grid: { color: '#303A52' },
                        ticks: { color: '#CBD5E1' }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: '#303A52' },
                        ticks: { color: '#CBD5E1' }
                    }
                },
                plugins: {
                    legend: {
                        labels: { color: '#CBD5E1' }
                    }
                }
            }
        });
    }
}
