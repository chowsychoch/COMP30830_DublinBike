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
    elem.setAttribute('id', 'select-box')
    elem.setAttribute('aria-label', 'Default select example')
    // elem.setAttribute('onChange', 'myNewFunction(this)')
    elem.setAttribute('name', 'number')
    elem.innerHTML += `
    <option value="" >Select a Station</option>
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
    // showPredict(id)
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
       var weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
        // get the weekday
        for (var [key, value] of weekMap) {
            if (key == 1) {
                average_week_data[0] += value;
            } else if (key == 2) {
                average_week_data[1] += value;
            } else if (key == 3) {
                average_week_data[2] += value;
            } else if (key == 4) {
                average_week_data[3] += value;
            } else if (key == 5) {
                average_week_data[4] += value;
            } else if (key == 6) {
                average_week_data[5] += value;
            } else if (key == 7) {
                average_week_data[6] += value;
            }
        }
        let name = average_day_bike[0].name;
        createChart('line', 'Daily Average Bikes Available:' + name, weekdays, average_week_data, "average_day_chart", 'rgba(255, 99, 132, 0.2)', 'rgba(153, 102, 255, 1)');
    });
}


function showPredict(id) {
    $.getJSON('/predict/' + id, predict_object => {
        let week_predict = predict_object['weekOfDay']
        console.log(week_predict)
        // get the data from tuple, first get labels
        var weekday = new Array();
        var weekday_bikeStands = new Array();
        var y_labels_bikeStand = new Array();
        var y_labels = new Array();
        // var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        for (var i in week_predict) {
            if (i == "Mon") {
                let temp1 = predict_object['weekOfDay']['Mon']['hour'];
                // temp1 = 'hour' :{1 : {"ava_bikes": 30}, 2: {"ava_bikes" : 20}, .....}
                for (var j1 in temp1) {
                    // j = 1 : {}, 2:{}, 3:{}.......
                    let hour_bike1 = predict_object['weekOfDay']['Mon']['hour'][j1]['ava_bikes'];
                    let hour_bikeStands1 = predict_object['weekOfDay']['Mon']['hour'][j1]['ava_stands'];
                    weekday.push(j1 +":00 Mon");
                    y_labels.push(hour_bike1);
                    y_labels_bikeStand.push(hour_bikeStands1);
                }
            }
            if (i == "Tue") {
                let temp2 = predict_object['weekOfDay']['Tue']['hour'];
                // temp1 = 'hour' :{1 : {"ava_bikes": 30}, 2: {"ava_bikes" : 20}, .....}
                for (var j2 in temp2) {
                    let hour_bike2 = predict_object['weekOfDay']['Tue']['hour'][j2]['ava_bikes']
                    let hour_bikeStands2 = predict_object['weekOfDay']['Tue']['hour'][j2]['ava_stands'];
                    weekday.push(j2+":00 Tue");
                    y_labels.push(hour_bike2);
                    y_labels_bikeStand.push(hour_bikeStands2);
                }
            }
            if (i == "Wed") {
                let temp3 = predict_object['weekOfDay']['Wed']['hour'];
                // temp1 = 'hour' :{1 : {"ava_bikes": 30}, 2: {"ava_bikes" : 20}, .....}
                for (var j3 in temp3) {
                    let hour_bike3 = predict_object['weekOfDay']['Wed']['hour'][j3]['ava_bikes'];
                    let hour_bikeStands3 = predict_object['weekOfDay']['Wed']['hour'][j3]['ava_stands'];
                    weekday.push(j3 +":00 Wed");
                    y_labels.push(hour_bike3);
                    y_labels_bikeStand.push(hour_bikeStands3);
                }
            }
            if (i == "Thu") {
                let temp4 = predict_object['weekOfDay']['Thu']['hour'];
                // temp1 = 'hour' :{1 : {"ava_bikes": 30}, 2: {"ava_bikes" : 20}, .....}
                for (var j4 in temp4) {
                    let hour_bike4 = predict_object['weekOfDay']['Thu']['hour'][j4]['ava_bikes'];
                    let hour_bikeStands4 = predict_object['weekOfDay']['Thu']['hour'][j4]['ava_stands'];
                    weekday.push(j4 +":00 Thurs");
                    y_labels.push(hour_bike4);
                    y_labels_bikeStand.push(hour_bikeStands4);
                }
            }
            if (i == "Fri") {
                let temp5 = predict_object['weekOfDay']['Fri']['hour'];
                for (var j5 in temp5) {
                    // j = 1 : {}, 2:{}, 3:{}.......
                    let hour_bike5 = predict_object['weekOfDay']['Fri']['hour'][j5]['ava_bikes'];
                    let hour_bikeStands5 = predict_object['weekOfDay']['Fri']['hour'][j5]['ava_stands'];
                    weekday.push(j5+":00 Fri");
                    y_labels.push(hour_bike5);
                    y_labels_bikeStand.push(hour_bikeStands5);
                }
            }
            if (i == "Sat") {
                let temp6 = predict_object['weekOfDay']['Sat']['hour'];
                // temp1 = 'hour' :{1 : {"ava_bikes": 30}, 2: {"ava_bikes" : 20}, .....}
                for (var j6 in temp6) {
                    let hour_bike6 = predict_object['weekOfDay']['Sat']['hour'][j6]['ava_bikes'];
                    let hour_bikeStands6 = predict_object['weekOfDay']['Sat']['hour'][j6]['ava_stands'];
                    weekday.push(j6+":00 Sat");
                    y_labels.push(hour_bike6);
                    y_labels_bikeStand.push(hour_bikeStands6);
                }
            }
            if (i == "Sun") {
                let temp7 = predict_object['weekOfDay']['Sun']['hour'];
                // temp1 = 'hour' :{1 : {"ava_bikes": 30}, 2: {"ava_bikes" : 20}, .....}
                for (var j7 in temp7) {
                    let hour_bike7 = predict_object['weekOfDay']['Sun']['hour'][j7]['ava_bikes'];
                    let hour_bikeStands7 = predict_object['weekOfDay']['Sun']['hour'][j7]['ava_stands'];
                    weekday.push(j7 +":00 Sun");
                    y_labels.push(hour_bike7);
                    y_labels_bikeStand.push(hour_bikeStands7);
                }
            }
        }
        console.log(weekday)
        console.log(y_labels)
        console.log('bike stn',y_labels_bikeStand)
        createChart('line', 'Predict Bikes Available, StationID:' + predict_object['station_id'], weekday, y_labels, "predict_chart");
        createChart('line', 'Predict Bikes Stands Available, StationID:' + predict_object['station_id'], weekday, y_labels_bikeStand, "predict_chart_stands");
    });
}

function GMTToDay(time) {
    let date = new Date(time)
    let Str = date.getFullYear() + '-' +
        (date.getMonth() + 1) + '-' +
        date.getDate()
    return Str
}


function createChart(chartType, title, labels, data, elementId, borderColor = 'rgb(75, 192, 192)') {
    var ctx = document.getElementById(elementId).getContext('2d');
    var chartConfig = {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                borderWidth:3,
                // backgroundColor: backgroundColor,
                fill: false,
                // tension: 0.1,
                borderColor: borderColor
            }]
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                        // This more specific font property overrides the global property
                        font: {
                            size: 14
                        }
                    }
                }
            },
            animation: {
                onComplete: null
            },
            legend: {
                display: false,
            },
            title: {
                position: 'top',
                display: true,
                text: title,
                fontFamily: "'Montserrat', sans-serif",
                size:20
            },
            scales: {
                xAxes: [{
                    gridLines: {
                        drawOnChartArea: false,
                    },
                    ticks:{
                        fontFamily:"'Montserrat', sans-serif"
                    }
                    // pointLabels: {
                    //     fontFamily: "'Montserrat', sans-serif"
                    // },
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        fontFamily: "'Montserrat', sans-serif"
                    },
                    // pointLabels: {
                    //     fontFamily: "'Montserrat', sans-serif"
                    // },
                    gridLines: {
                        drawOnChartArea: false
                    }
                }]
            }
        }
    };
    charts = new Chart(ctx, chartConfig);
    return charts;
}



// document.querySelector('#user-query')
// .addEventListener('submit',async function(event){
//     event.preventDefault();

//     // Serialize the Form afterwards
//     const form = this;
//     const formObject = {};
//     for(let input of form){
//         if(!['submit','reset'].includes(input.type)){
//             formObject[input.name] = input.value;
//         }
//     }
//     const res = await fetch('/predict',{
//         method:"POST",
//         headers:{
//             "Content-Type":"application/json"
//         },
//         body: JSON.stringify(formObject)
//     });
//     const result = await res.json();
//     console.log(result);
// })

async function userResult() {
    var e = document.getElementById("select-box");
    var id = e.value;
    showPredict(id)

}