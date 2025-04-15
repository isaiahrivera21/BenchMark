document.addEventListener('DOMContentLoaded', function() {
    // Establish WebSocket connection
    const wsUrl = 'ws://' + window.location.host + '/ws/all_time_macros/';
    const socket = new WebSocket(wsUrl);

    // Connection opened
    socket.onopen = function(event) {
        console.log('WebSocket connection established');
    };

    // Listen for messages
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const macros = data.data;

        // Update the UI with macro data
        document.getElementById('average-calories').textContent = macros.average_calories || 'N/A';
        document.getElementById('average-fat').textContent = macros.average_fat || 'N/A';
        document.getElementById('average-carbs').textContent = macros.average_carbohydrates || 'N/A';
        document.getElementById('average-protein').textContent = macros.average_protien || 'N/A';
        document.getElementById('average-cholesterol').textContent = macros.average_cholesterol || 'N/A';
        document.getElementById('average-sodium').textContent = macros.average_sodium || 'N/A';
    };

    // Connection error
    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    // Connection closed
    socket.onclose = function(event) {
        console.log('WebSocket connection closed');
    };
});