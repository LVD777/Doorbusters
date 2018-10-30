/* global var
============================================= */
const URL_BFA_YEARS      = "http://bootcamp.brogard.io:5051/years";

var selectYear = d3.select("#bbb--select-year");
var selectCategory = d3.select("#bbb--select-category");

// loader settings
var opts = {
  lines: 9, // The number of lines to draw
  length: 9, // The length of each line
  width: 5, // The line thickness
  radius: 14, // The radius of the inner circle
  color: '#EE3124', // #rgb or #rrggbb or array of colors
  speed: 1.9, // Rounds per second
  trail: 40, // Afterglow percentage
  className: 'spinner', // The CSS class to assign to the spinner
}; 


//****************** init *****************************//
var spinner;

init();

//****************** Event Listeners ******************//

selectYear.on("change", function() {
    var thisCategory = selectCategory.node().value;
    
    console.log("### selectYear     select value => "+this.value);
    console.log("    selectCategory select value => "+thisCategory);

    plotPie(this.value, thisCategory);
    plotBubble(this.value, thisCategory);
    //plotGuage(this.value);
    //
    
    selectCategory.selectAll("option").remove();
    renderSelectCategories(this.value);
});

selectCategory.on("change", function() {
    var thisYear = selectYear.node().value;

    console.log("### selectCategory select value => "+this.value);
    console.log("    selectYear     select value => "+thisYear);

    plotPie(thisYear, this.value);
    plotBubble(thisYear, this.value);
    //plotGuage(this.value);
    //
    //refreshMetadata(this.value);    
});


/* Functions
============================================= */

/*
 * start the show
 */
function init() {
    var target = document.getElementById("bbb--middle");
    var spinner = new Spinner(opts).spin(target);
    
    renderSelectYears();
    
    var thisCategory = "APPAREL";
    var thisYear = 2017;
    
    plotPie(thisYear, thisCategory);
    plotBubble(thisYear, thisCategory);
    spinner.stop();
}

/*
 * makes API call to fetch 
 * sample data names
 */
function renderSelectYears() {
    
    d3.json(URL_BFA_YEARS, function(obj) {
        select = d3.select("#bbb--select-year")
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
        renderSelectCategories(thisYear);
    });
}

function renderSelectCategories(year) {
    var url = `http://bootcamp.brogard.io:5051/categories/${year}/year`;
    
    d3.json(url, function(obj) {
        d3.select("#bbb--select-category")
            .selectAll("option")
            .data(obj)
            .enter()
            .append("option")
            .text(function (d) {
                return d;
            }).attr("value", function(d) {
                return d;
            }).attr("data", year);
    });    
}


/*
 * pie chart plot
 */
function plotPie(year, category) {
    var url = `http://bootcamp.brogard.io:5051/ads/${year}/year/${category}/category`;

    d3.json(url, function(dataset) {
        var div = document.getElementById("bbb--pie-chart");

        var prices = dataset.plot.prices;
        var items  = dataset.plot.items;
        var stores = dataset.plot.stores;

        var sliceValues = prices.slice(0,25);
        var sliceItems = items.slice(0,25);
        var sliceStores = stores.slice(0,25);

        var trace = {
            values: prices,
            labels: stores,
            type: 'pie',
            text: items,
            textinfo: 'percent',
            hoverinfo: 'label+text+percent'
        };        
        
        var trace1 = {
            values: sliceValues,
            labels: sliceStores,
            type: 'pie',
            text: sliceItems,
            textinfo: 'percent',
            hoverinfo: 'label+text+percent'
        };

        var layout = {
            title: "<b>Top Stores for <i>"+category+"</i> in "+ year + "</b>"
        };

        var plotData = [trace1];
          
        Plotly.newPlot(div, plotData, layout);
    });
}

/*
 * bubble chart plot
 */
function plotBubble(year, category) {
    var url = `http://bootcamp.brogard.io:5051/ads/${year}/year/${category}/category`;
    
    d3.json(url, function(dataset) {
        var div = document.getElementById("bbb--bubble-chart");
        
        var prices = dataset.plot.prices;
        var items  = dataset.plot.items;
        var stores = dataset.plot.stores;

        var trace = {
            x: prices,
            y: stores.length,
            text: items,
            hoverinfo: "x+y+text+percent",
            mode: "markers",
            marker: {
                size: (Math.sqrt(prices*15))
            }
        };

        var layout = {
            title: "<b>Ads for <i>"+category+"</i> in "+ year + "</b>",
            margin: {
                l: 40,
                r: 40,
                pad: 0
            },
        };

        var plotData = [trace];
          
        Plotly.newPlot(div, plotData, layout);
    });
}

/*
 * guage chart plot
 */
function plotGuage(sample) {
    var url = URL_SAMPLE_WFREQ + sample;
    
    d3.json(url, function(data) {
        var div = document.getElementById("bbb--gauge-chart");
    
        // Enter a speed between 0 and 9
        var level = data;
        
        // Trig to calc meter point
        var degrees = 180 - level*20,
            radius = 0.5;
        var radians = degrees * Math.PI / 180;
        var x = radius * Math.cos(radians);
        var y = radius * Math.sin(radians);
        
        // Path: may have to change to create a better triangle
        var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
            pathX = String(x),
            space = ' ',
            pathY = String(y),
            pathEnd = ' Z';
        var path = mainPath.concat(pathX, space, pathY, pathEnd);

        var plotData = [{
                type: 'scatter',
                x: [0],
                y: [0],
                marker: {
                    size: 28,
                    color: 'DB5F59'
                },
                showlegend: false,
                name: 'speed',
                text: level,
                hoverinfo: 'text+name'
            },
            {
                values: [50 / 9, 50 / 9, 50 / 9, 50 / 9, 50 / 9, 50 / 9,50 / 9, 50 / 9, 50 / 9, 50],
                rotation: 90,
                text: ['8-9', '7-8', '6-7', '5-6', '4-5', '3-4', '2-3', '1-2', '0-1', ''],
                textinfo: 'text',
                textposition: 'inside',
        
                marker: {
                    colors: ['rgba(14, 127, 0, .5)',    'rgba(110, 154, 22, .5)', 'rgba(173, 255, 186, .5)',
                             'rgba(170, 202, 42, .5)',  'rgba(202, 209, 95, .5)', 'rgba(122, 255, 142, .5)',
                             'rgba(210, 206, 145, .5)', 'rgba(232, 226, 202, .5)','rgba(97, 255, 121, .5)',
                             'rgba(255, 255, 255, 0)'
                    ]
                },
                labels: ['8-9', '7-8', '6-7', '5-6', '4-5', '3-4', '2-3', '1-2', '0-1', ''],
                hoverinfo: 'label',
                hole: 0.5,
                type: 'pie',
                showlegend: false
            }];

        var layout = {
            autosize: true,
            showlegend: false,
            shapes: [{
                type: 'path',
                path: path,
                fillcolor: 'DB5F59',
                line: {
                    color: 'DB5F59'
                }
            }],
            title: '<b>Belly Button Weekly Washing Frequency</b> <br> Scrubs per Week',
            xaxis: {
                zeroline: false,
                showticklabels: false,
                showgrid: false,
                range: [-1, 1]
            },
            yaxis: {
                zeroline: false,
                showticklabels: false,
                showgrid: false,
                range: [-1, 1]
            }
        };
        
        Plotly.newPlot(div, plotData, layout);
    });        
}

