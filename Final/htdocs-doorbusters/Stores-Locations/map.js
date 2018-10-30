/* Global Constants
============================================= */
const MAPBOX_API_KEY = "pk.eyJ1IjoiY2doYXllczk5IiwiYSI6ImNqbjB4cXF3bDAzZHQzcW84NjZwaWtzYWEifQ.FNyqY-OeU-ofKd8GMBgwww";

const LAYER_OUTDOORS = L.tileLayer(`https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?access_token=${MAPBOX_API_KEY}`, {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, " +
                 "<a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © "+
                 "<a href=\"https://www.mapbox.com/\">Mapbox</a>",
    id: "mapbox.streets",
    maxZoom: 18,
});

const LAYER_SATELLITE = L.tileLayer(`https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{z}/{x}/{y}?access_token=${MAPBOX_API_KEY}`, {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, " +
                 "<a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © "+
                 "<a href=\"https://www.mapbox.com/\">Mapbox</a>",
    id: "mapbox.streets",
    maxZoom: 18,
});

const LAYER_LIGHT = L.tileLayer(`https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=${MAPBOX_API_KEY}`, {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, " +
                 "<a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © "+
                 "<a href=\"https://www.mapbox.com/\">Mapbox</a>",
    id: "mapbox.streets",
    maxZoom: 18,
});

const LAYER_STREET = L.tileLayer(`https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=${MAPBOX_API_KEY}`, {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, " +
                 "<a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © "+
                 "<a href=\"https://www.mapbox.com/\">Mapbox</a>",
    id: "mapbox.streets",
    maxZoom: 18,
});

const URL_BFA_YEARS = "http://bootcamp.brogard.io:5051/years";

var selectYear = d3.select("#bbb--select-year");
var selectStore = d3.select("#bbb--select-store");

/* Global Var
============================================= */
var heatLayer;
var map = L.map("map").setView([39.095963, -97.734375], 5);

renderSelectStores();
renderSelectYears();
 
//****************** init *****************************//

//****************** main ******************//
renderHeatMap(2017, "TARGET");


//****************** Event Listeners ******************//
selectYear.on("change", function() {
    var thisStore = selectStore.node().value;
    console.log("### selectYear  select value => "+this.value);
    console.log("    selectStore select value => "+thisStore);
    updateHeatMap(this.value, thisStore);
});

selectStore.on("change", function() {
    var thisYear = selectYear.node().value;
    console.log("### selectStore   select value => "+this.value);
    console.log("    selectYear     select value => "+thisYear);
    updateHeatMap(thisYear, this.value);
});


/* Functions
============================================= */
function renderHeatMap(year, store) {
    url = `http://bootcamp.brogard.io:5051/geo/stats/${year}/year/${store}/store`;
    d3.json(url, function(data) {
        heatLayer = L.heatLayer(data, {radius: 20});    

        LAYER_LIGHT.addTo(map);
        heatLayer.addTo(map);
    });
}

function updateHeatMap(year, store) {
    heatLayer.remove();
    url = `http://bootcamp.brogard.io:5051/geo/stats/${year}/year/${store}/store`;
    d3.json(url, function(data) {
        heatLayer = L.heatLayer(data, {radius: 20});
        heatLayer.addTo(map);
    });
}

function renderSelectYears() {
    d3.json(URL_BFA_YEARS, function(obj) {
        var select = d3.select("#bbb--select-year")
            .selectAll("option")
            .data(obj)
            .enter()
            .append("option")
            .text(function (d) {
                return d;
            }).attr("value", function(d) {
                return d;
            });
        var thisYear = select.node().value;
        renderSelectStores(thisYear);
    });
}

function renderSelectStores(year) {
    var url = `http://bootcamp.brogard.io:5051/stores/${year}/year`;
    d3.json(url, function(obj) {
        d3.select("#bbb--select-store")
            .selectAll("option")
            .data(obj)
            .enter()
            .append("option")
            .text(function (d) {
                return d;
            }).attr("value", function(d) {
                return d;
            });
    });
}
