document.addEventListener('DOMContentLoaded', function() {
    const wsUrl = 'ws://' + window.location.host + '/ws/weekly_macros/';
    const socket = new WebSocket(wsUrl);

    socket.onopen = function(event) {
        console.log('Weekly Macros WebSocket connection established');
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const macros = data.data;

        document.getElementById('weekly-average-calories').textContent = macros.average_calories || 'N/A';
        document.getElementById('weekly-average-fat').textContent = macros.average_fat || 'N/A';
        document.getElementById('weekly-average-carbs').textContent = macros.average_carbohydrates || 'N/A';
        document.getElementById('weekly-average-protein').textContent = macros.average_protien || 'N/A';
        document.getElementById('weekly-average-cholesterol').textContent = macros.average_cholesterol || 'N/A';
        document.getElementById('weekly-average-sodium').textContent = macros.average_sodium || 'N/A';
    };

    socket.onclose = function(event) {
        console.log('Weekly Macros WebSocket connection closed');
    };
});