console.log('dynamic mycafe happening');

socket = new WebSocket('ws://' + window.location.host + '/ws/dynamicMycafe/');

socket.onmessage = function(e) {
    console.log('Meal_id Reserved: ' + e.data);
    // console.log(typeof e.data)
    const meal_id = JSON.parse(e.data).message
    console.log(meal_id)
    var numres = document.getElementById("numres" + meal_id);
    if (numres !== null) {
        numres.textContent = (parseInt(numres.textContent) + 1).toString();
    }
};