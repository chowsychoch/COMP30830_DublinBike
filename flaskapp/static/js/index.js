let map;
var charts = null

// Initialize and add the map
function initMap() {
    var hashmap = new Map();
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
        for (let item of data) {
            let number = item['number']
            item = new google.maps.Marker({
                position: { lat: item['pos_lat'], lng: item['pos_lng'] },
                map: map,
            })
            hashmap.set(number, item);
        }
        // iterate th map, pass the key and value to click function
        for (var entry of hashmap) {
            let [number, i] = entry
            // pass the number of station and marker， add listener function
            // when click the marker, call showClick
            i.addListener("click", () => showClick(number, i));
        }
        printUserOption(data)
    }).catch(err => {
        console.log("Map Err", err);
    })

}
/*function printMarker(data) {
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
        // const cityCircle = new google.maps.Circle({
        //     strokeColor: "#FF0000",
        //     strokeOpacity: 0.8,
        //     strokeWeight: 2,
        //     fillColor: "#FF0000",
        //     fillOpacity: 0.35,
        //     map,
        //     center: { lat: 41.878, lng: -87.629 },
        //     radius: 100
        //   });
    }

}*/

function printUserOption(data) {
    const elem = document.createElement('select');
    elem.setAttribute('class', 'form-select')
    elem.setAttribute('aria-label', 'Default select example')
    elem.innerHTML += `
    <option selected>Select a Station</option>
    `
    for (let item of data) {
        elem.innerHTML += `
        <option value="${item['number']}">${item['name']}</option>
        `
    }
    elem.innerHTML += `<input class="btn btn-primary" type="submit" value="Submit">`

    const option = document.getElementById("option")
    option.appendChild(elem)
}

function showClick(id, i) {
    //print marker
    printMarker(id, i)
    showChartDaily(id)
}

function printMarker(id, i) {
    // get the message of this station of id
    fetch("/stations/" + id).then(response => {
        return response.json()
    }).then(data => {
        const contentString = `
        <div id="content">Name: ${data[0].name}</div>
        <div class="info">Address: ${data[0].address}</div>
        <div class="info">Available Bikes: ${data[0].available_bikes}</div>
        <div class="info">Bike stands: ${data[0].available_bike_stands}</div>
        `
        const infoWindow = new google.maps.InfoWindow({
            content: contentString
        })
        infoWindow.open(map, i);
    })
}

// show the daily chart
function showChartDaily(id) {
    // get labels and data
    let weekMap = new Map();
    $.getJSON('/occupancy/' + id, average_day_bike => {
        // parse json to an object
        for (var i in average_day_bike) {
            var day = average_day_bike[i].Weekday;
            var array_bike = average_day_bike[i].available_bikes;
            if (weekMap.has(day)) {
                let temp = weekMap.get(day)
                weekMap.set(day, array_bike + temp);
            } else {
                weekMap.set(day, array_bike);
            }
            // var date = new Date(average_day_bike[i].last_update);
            // let time = GMTToDay(date)
            // labels.push(time)
        }
        // define new labels, initialize the array
        var average_week_data = new Array(7)
        for (let i = 0; i < 7; i++) {
            average_week_data[i] = 0;
        }
        var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        // get the weekday
        for (var [key, value] of weekMap) {
            if (key == 1) {
                average_week_data[1] += value;
            } else if (key == 2) {
                average_week_data[2] += value;
            } else if (key == 3) {
                average_week_data[3] += value;
            } else if (key == 4) {
                average_week_data[4] += value;
            } else if (key == 5) {
                average_week_data[5] += value;
            } else if (key == 6) {
                average_week_data[6] += value;
            } else if (key == 7) {
                average_week_data[0] += value;
            }
        }
        let name = average_day_bike[0].name;
        createChart('line', 'Daily Average Bikes Available:' + name, weekdays, average_week_data, "average_day_chart", 'rgba(255, 99, 132, 0.2)', 'rgba(153, 102, 255, 1)');
    });
}

function GMTToDay(time) {
    let date = new Date(time)
    let Str = date.getFullYear() + '-' +
        (date.getMonth() + 1) + '-' +
        date.getDate()
    return Str
}


function createChart(chartType, title, labels, data, elementId, backgroundColor = 'rgba(102, 122, 205, 0.2)', borderColor = 'rgba(54, 162, 235, 1)') {
    if (charts) {
        charts.destroy();
    }
    var ctx = document.getElementById(elementId).getContext('2d');
    var chartConfig = {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: 1
            }]
        },
        options: {
            animation: {
                onComplete: null
            },
            legend: {
                display: false
            },
            title: {
                position: 'top',
                display: true,
                text: title
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    };
    charts = new Chart(ctx, chartConfig);
    return charts;
}
