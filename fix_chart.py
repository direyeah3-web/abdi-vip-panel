# fix_chart.py - Hagaaji renderChart si uu u isticmaalo weeklyData

with open("public/index.html", "r") as f:
    content = f.read()

# Hel renderChart hore
start = content.find("function renderChart(d)")
end = content.find("function handleLogout()")

if start != -1 and end != -1:
    new_chart = '''function renderChart(d){
    var c=document.getElementById('analyticsChart');
    if(c){
        if(window.myChart)window.myChart.destroy();
        var weekly = d.weeklyData || [0,0,0,0,0,0,0];
        window.myChart=new Chart(c.getContext('2d'),{
            type:'line',
            data:{
                labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
                datasets:[{
                    label:'New Users',
                    data:weekly,
                    borderColor:'#00d4ff',
                    backgroundColor:'rgba(0,212,255,0.1)',
                    tension:0.4,
                    fill:true,
                    borderWidth:2
                }]
            },
            options:{
                responsive:true,
                plugins:{legend:{display:false}},
                scales:{
                    y:{beginAtZero:true,grid:{color:'#1e1e2a'},ticks:{color:'#6b6b7e'}},
                    x:{grid:{display:false},ticks:{color:'#6b6b7e'}}
                }
            }
        });
    }
    
    var c2=document.getElementById('licenseChart');
    if(c2){
        if(window.licenseChart)window.licenseChart.destroy();
        var unused = d.unusedLicenses || 0;
        var used = d.usedLicenses || 0;
        if(unused === 0 && used === 0){
            c2.parentElement.innerHTML = '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:200px;color:var(--muted);"><i class="fa-solid fa-chart-pie" style="font-size:40px;margin-bottom:15px;opacity:0.3;"></i><p>No license data yet</p></div>';
        } else {
            window.licenseChart=new Chart(c2.getContext('2d'),{
                type:'doughnut',
                data:{
                    labels:['Available','Used'],
                    datasets:[{
                        data:[unused,used],
                        backgroundColor:['#10b981','#f59e0b'],
                        borderWidth:0
                    }]
                },
                options:{
                    responsive:true,
                    plugins:{legend:{position:'bottom',labels:{color:'#6b6b7e',padding:15}}},
                    cutout:'70%'
                }
            });
        }
    }
}
'''
    
    content = content[:start] + new_chart + content[end:]
    with open("public/index.html", "w") as f:
        f.write(content)
    print("✅ renderChart waa la hagaajiyay!")
else:
    print("❌ Ma helin renderChart")
