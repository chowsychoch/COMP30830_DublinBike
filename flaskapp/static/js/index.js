let map;
// Initialize and add the map
function initMap() {
    fetch("/station").then(response => {
        //call the get api to get all stations point first
        return response.json()
    }).then(data => {
        //add the map 
        map = new google.maps.Map(document.getElementById("map"), {
            //disable default clickable landmark
            clickableIcons: false,
            center: { lat: 53.347777, lng: -6.244239 },
            zoom: 14,
        });
        //print marker
        printMarker(data)
    }).catch(err => {
        console.log("Map Err", err);
    })

}
function printMarker(data) {
    //loop over result and pass it to marker
    for (let item of data) {
        //info box of each marker
        const contentString = `
        <div id="content">Name: ${item['name']}</div>
        <div class="info">Address: ${item['address']}</div>
        <div class="info">Available Bikes: ${item['available_bikes']}</div>
        <div class="info">Bike stands: ${item['bike_stands']}</div>
        `
        const infoWindow = new google.maps.InfoWindow({
            content: contentString
        })

        item = new google.maps.Marker({
            position: { lat: item['pos_lat'], lng: item['pos_lng'] },
            map: map,
        })
        item.addListener("click", () => {
            infoWindow.open(map, item);
        })
    }

}
