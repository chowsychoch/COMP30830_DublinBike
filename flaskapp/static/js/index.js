let map;
// Initialize and add the map
function initMap() {
    fetch("/station").then(response => {
        //call the get api to get all stations point first
        return response.json()
    }).then(data => {
        // console.log("data: ", data);
        //add the map 
        map = new google.maps.Map(document.getElementById("map"), {
            //disable default clickable landmark
            clickableIcons: false,
            center: { lat: 53.347777, lng: -6.244239 },
            zoom: 14,
        });
        //loop over result and pass it to marker
        for (let item of data) {
            new google.maps.Marker({
                position: { lat: item['pos_lat'], lng: item['pos_lng'] },
                map: map,
            })
        }
    }).catch(err => {
        console.log("Map Err", err);
    })

}
