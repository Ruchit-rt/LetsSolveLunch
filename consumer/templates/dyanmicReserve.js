console.log('dynamic reserve happening')

socket = new WebSocket('ws://' + window.location.host + '/ws/dynamic/')
console.log(document.getElementById("meal_id").textContent)
socket.onopen = function(e) {
    socket.send(JSON.stringify({
        'message': document.getElementById("meal_id").textContent,
    }));
};