$(document).ready(function() {
    console.log("Page Loaded");
    doWork();
    //my event listener for my drop down
    $("#selDataset").on("change", function(){
	    doWork()
    });

});

function doWork() {
    // Read in the data using ajax
    //week 14, day 3, activity 2 referencing 
    var url = "static/data/samples.json";
    requestAjax(url);
}

function requestAjax(url) {
    $.ajax({
        type: "GET",
        url: url,
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            console.log(data);
            //create all my charts
            createDropdown(data);
            createMetadata(data);
            createBarChart(data);
            createBubbleChart(data);
            createGaugebonus(data);
            
        },
        error: function(textStatus, errorThrown) {
            console.log("FAILED to get data");
            console.log(textStatus);
            console.log(errorThrown);
        }
    });
}

//Make the test Subject ID drop down first since all other charts depend on it
function createDropdown(data) {
    var names = data.names;
    for (let i = 0; i < names.length; i++) {
        let name = names[i];
        let html = `<option>${name}</option>`;
        $("#selDataset").append(html);
    }
}
//make the demographic info
function createMetadata(data) {
    $("#sample-metadata").empty();// this will clear the before demographic data and not continue to append after each selection
    let id = $("#selDataset").val();//getting the current selected id from drop down
    //only want == because drop down is string and meta data is a int. They are different types so === would fail
    //https://www.guru99.com/difference-equality-strict-operator-javascript.html
    let info = data.metadata.filter(x => x.id == id)[0];
    Object.entries(info).map(function(x) {
        let html = `<h6>${x[0]}: ${x[1]}</h6>`;//.map =looping through each item. want both key and accordingly output
        $("#sample-metadata").append(html);
    
    });
}
//Make the barchart
function createBarChart(data) {
    let id = $("#selDataset").val();
    let sample = data.samples.filter(x => x.id == id)[0];

    var trace1 = {
        type: 'bar',
        x: sample.sample_values.slice(0, 10).reverse(),
        y: sample.otu_ids.map(x => `OTU ${x}`).slice(0, 10).sort().reverse(),
        //only want the top 10 and sort largest to lowest with reverse
        //https://www.w3schools.com/jsref/jsref_reverse.asp, https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
        text: sample.otu_labels.slice(0, 10).reverse(),
        orientation: 'h',//horizonatal
        marker: {
            color: '#2aa198',
            width: 1
          }

    }

    var datab = [trace1];
    var layout = {
        // title: "Top 10 OTUs Found",
        xaxis:{title:{text:"Count"},},
        yaxis:{title:{text:"OTU ID"},},
    }

    Plotly.newPlot('barchart', datab, layout);
}
//Make the bubblechart
function createBubbleChart(data) {
    let id = $("#selDataset").val();
    let sample = data.samples.filter(x => x.id == id)[0];

    var trace1 = {
        x: sample.otu_ids,
        y: sample.sample_values,
        text: sample.otu_labels.slice(0, 10).reverse(),//reverse to flip chart like example wanted
        mode: 'markers',
        marker: {
            size: sample.sample_values,
            color: sample.otu_ids,
            colorscale: 'YlGnBu'
            // '#2aa198', for plain
            // colorscale:'YlGnBu', https://plotly.com/javascript/colorscales/
        }
    }

    var datab = [trace1];
    var layout = {
        // "title": "Bubble Chart Placeholder"
        xaxis:{title:{text:"OTU ID"},},
        yaxis:{title:{text:"Count"},},
    }

    Plotly.newPlot('bubblechart', datab, layout);
}

// BONUS 
// Gauge Chart to plot weekly washing frequency 
// https://plotly.com/javascript/gauge-charts/
function createGaugebonus(data) {
    let id = $("#selDataset").val();
    let sample = data.metadata.filter(x => x.id == id)[0];

    var trace1 = {
          domain: { x: [0,1], y: [0,1]},
          value: sample["wfreq"],
          type: "indicator",
          mode: "gauge+number+delta",
        //   delta: { reference: 2.5},//this is the average. all ID's will be compared to this
          gauge: {
            axis: { range: [null, 9] },
            bar: {color: '#2aa198'},
            steps: [
                { range: [0, 1], color: "#e5d5d0" },
                { range: [1, 2], color: "#dbc7c2" },
                { range: [2, 3], color: "#d2b9b4" },
                { range: [3, 4], color: "#c9ada7" },
                { range: [4, 5], color: "#ac9899" },
                { range: [5, 6], color: "#8a7e88" },
                { range: [6, 7], color: "#7d7482" },
                { range: [7, 8], color: "#706a7b" },
                { range: [8, 9], color: "#4a4e69" }
            ],
            threshold: {
            //   line: { color: "white", width: 4 },
            //   thickness: 1.0,
              value: 9
            }
          }
        }
    var datag = [trace1];
      
      Plotly.newPlot('gauge', datag);
}

