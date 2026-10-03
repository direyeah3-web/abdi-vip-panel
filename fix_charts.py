# fix_charts.py - Hagaaji renderCharts function

with open("public/index.html", "r") as f:
    content = f.read()

start = content.find("function renderCharts(data)")
end = content.find("function handleLogout()")

if start != -1 and end != -1:
    new_charts = '''function renderCharts(data) {
        var ctx1 = document.getElementById('analyticsChart');
        if (ctx1) {
            if (window.analyticsChartInstance) window.analyticsChartInstance.destroy();
            window.analyticsChartInstance = new Chart(ctx1.getContext('2d'), {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Active Users',
                        data: [1, 2, 3, 4, 5, 6, data.totalUsers || 0],
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, grid: { color: '#2a2a35' }, ticks: { color: '#8b8b9e' } },
                        x: { grid: { display: false }, ticks: { color: '#8b8b9e' } }
                    }
                }
            });
        }
        
        var ctx2 = document.getElementById('licenseChart');
        if (ctx2) {
            if (window.licenseChartInstance) window.licenseChartInstance.destroy();
            window.licenseChartInstance = new Chart(ctx2.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: ['Unused', 'Used'],
                    datasets: [{
                        data: [data.unusedLicenses || 0, data.usedLicenses || 0],
                        backgroundColor: ['#10b981', '#f59e0b'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom', labels: { color: '#8b8b9e', padding: 15 } } },
                    cutout: '70%'
                }
            });
        }
    }
    
    '''
    content = content[:start] + new_charts + content[end:]
    with open("public/index.html", "w") as f:
        f.write(content)
    print("✅ renderCharts waa la cusboonaysiiyay!")
else:
    print("❌ Ma helin renderCharts")
