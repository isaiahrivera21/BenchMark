document.addEventListener('DOMContentLoaded', function() {
    // Load Chart.js from CDN with fallback
    if (typeof Chart === 'undefined') {
        console.error("Chart.js failed to load from CDN. Loading local fallback.");
        const script = document.createElement('script');
        script.src = "{% static 'js/chart.js' %}";
        document.head.appendChild(script);
    }

    // Initialize calorie chart
    const calorieTotal = parseInt('{{ daily_calories.value }}', 10) || 0;
    const calorieBalance = parseInt('{{ calorie_balance.value }}', 10) || 0;
    const calorieExpenditure = calorieBalance;

    // Custom plugin to display text in the center of the chart
    const centerTextPlugin = {
        id: 'centerText',
        afterDraw: function(chart) {
            if (chart.data.datasets[0].data.length === 0) return;

            const ctx = chart.ctx;
            const calorieBalance = parseInt('{{ calorie_balance.value }}', 10) || 0;
            const calorieTotal = parseInt('{{ daily_calories.value }}', 10) || 0;

            // Calculate balance status
            let statusText = '';
            if (calorieBalance > 0) {
                statusText = calorieBalance > calorieTotal * 0.25 ? 'Major Surplus' : 'Slight Surplus';
            } else if (calorieBalance < 0) {
                statusText = Math.abs(calorieBalance) > calorieTotal * 0.25 ? 'Major Deficit' : 'Slight Deficit';
            } else {
                statusText = 'Balanced';
            }

            ctx.save();
            ctx.font = 'bold 20px Arial';
            ctx.fillStyle = '#ffffff';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            const centerX = (chart.chartArea.left + chart.chartArea.right) / 2;
            const centerY = (chart.chartArea.top + chart.chartArea.bottom) / 2;

            // Display status text in center
            ctx.fillText(statusText, centerX, centerY);
            
            // Display calorie balance value below status
            ctx.font = 'bold 16px Arial';
            ctx.fillText(`Calorie Balance: ${calorieBalance}`, centerX, centerY + 30);
            ctx.restore();
        }
    };

    const ctx = document.getElementById('calorieChart').getContext('2d');
    const calorieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Calorie Intake', 'Calorie Expenditure'],
            datasets: [{
                data: [Math.abs(calorieBalance), calorieExpenditure],
                backgroundColor: [
                    calorieBalance >= 0 ? '#FF8C00' : '#4CAF50',
                    calorieBalance >= 0 ? '#4CAF50' : '#FF8C00'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#ffffff',
                        generateLabels: function(chart) {
                            const data = chart.data;
                            if (data.labels.length && data.datasets.length) {
                                return data.labels.map(function(label, i) {
                                    const meta = chart.getDatasetMeta(0);
                                    const style = meta.controller.getStyle(i);
                                    const value = data.datasets[0].data[i];
                                    const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
                                    const percentage = Math.round((value / total) * 100);
                                    
                                    return {
                                        text: `${label}: ${value} (${percentage}%)`,
                                        fillStyle: style.backgroundColor,
                                        strokeStyle: style.borderColor,
                                        lineWidth: style.borderWidth,
                                        hidden: false,
                                        index: i
                                    };
                                });
                            }
                            return [];
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            
                            if (context.index === 0) {
                                return `Calorie Intake: ${value} (${percentage}%)`;
                            } else {
                                return `Calorie Expenditure: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        },
        plugins: [centerTextPlugin]
    });
});