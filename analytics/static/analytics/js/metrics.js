document.addEventListener('DOMContentLoaded', function() {
    const wsUrl = 'ws://' + window.location.host + '/ws/metrics/';
    const socket = new WebSocket(wsUrl);

    socket.onopen = function(event) {
        console.log('WebSocket connection established');
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const metrics = data.data;

        // Update the UI with all metrics
        document.getElementById('volume-change').textContent = metrics.volume_change;
        document.getElementById('weight-per-rep-change').textContent = metrics.weight_per_rep_change;
        document.getElementById('rep-change').textContent = metrics.rep_change;
        document.getElementById('set-change').textContent = metrics.set_change;
    };

    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    socket.onclose = function(event) {
        console.log('WebSocket connection closed');
    };
});