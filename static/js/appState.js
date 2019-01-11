function buildStatedata(state) {

  var url = `/stats/${state}`

  console.log("---- buildStatedata initiated ----")

  // Use `d3.json` to fetch the metadata for a state
  d3.json(url).then(function(response) {
   
    // Use d3 to select the panel with id of `#state-loandata`
    var state_data = d3.select("#state-loandata");

    // Use `.html("") to clear any existing metadata
    state_data.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(response[0]).forEach(([key, value]) => {
      var cell = state_data.append("h6");
      cell.text(`${key}: ${value}`);
    });

  });
}

function buildCharts(state) {

  var url = `/status/${state}`

  console.log("---- buildCharts initiated ----")
  
  // Build a Pie Chart for the State Loan Status
  d3.json(url).then(function(response) {
    
    var s_labels = response.loan_status;
    var s_values = response.loan_counts;
    var s_hover = response.loan_status;
    
    var trace1 = {
        labels: s_labels,
        values: s_values,
        hovertext: s_hover,
        hoverinfo: 'hovertext',
        type: 'pie',
        showlegend: false
      };

    var data1 = [trace1];

    var layout1 = {
          title: "<b>Loan Status</b>",
        };

    Plotly.newPlot("pie1", data1, layout1);

  });

  var url1 = `/grades/${state}`

  // Build a Pie Chart for the State Loan Grades
  d3.json(url1).then(function(response1) {
    
    var s_labels = response1.grades;
    var s_values = response1.grade_counts;
    var s_hover = response1.grades;
    
    var trace2 = {
        labels: s_labels,
        values: s_values,
        hovertext: s_hover,
        hoverinfo: 'hovertext',
        type: 'pie',
      };

    var data2 = [trace2];

    var layout2 = {
          title: "<b>Loan Grades</b>",
        };

    Plotly.newPlot("pie2", data2, layout2);

  });

  var url2 = `/home/${state}`

  // Build a Bar Chart for the State Loans home ownership
  d3.json(url2).then(function(response2) {
    
    var x_axis = response2.owner_status;
    var y_axis = response2.owner_counts;
    
    var trace3 = {
        x: x_axis,
        y: y_axis,
        type: 'bar',
        marker: {
          color: 'rgb(142,124,195)'
        }
      };

    var data3 = [trace3];

    var layout3 = {
          title: "<b>Loan Home Ownership Status</b>",
          xaxis: {
            title: 'Status',
            tickangle: -45
          },
          yaxis: {
            title: 'Count'
          },
          bargap: 0.15
        };

    Plotly.newPlot("bar", data3, layout3);

  });
  
  var url3 = `/years/${state}`

  // Build a Line Chart for the State Loans per year
  d3.json(url3).then(function(response3) {
    
    var x_axis = response3.years;
    var y_axis = response3.loan_counts;
    
    var trace4 = {
        x: x_axis,
        y: y_axis,
        mode: 'lines',
        name: 'Lines'
      };

    var data4 = [trace4];

    var layout4 = {
          title: "<b>Loans per Year</b>",
          xaxis: {
            title: 'Years',
            nticks: 5
          },
          yaxis: {
            title: 'Loan Count'
          }
        };

    Plotly.newPlot("line", data4, layout4);

  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of state names to populate the select options
  d3.json("/states").then((stateNames) => {
    stateNames.forEach((state) => {
      selector
        .append("option")
        .text(state)
        .property("value", state);
    });

    // Use the first state from the list to build the initial plots
    const firstState = stateNames[0];
    buildCharts(firstState);
    buildStatedata(firstState);
  });
}

function optionChanged(newState) {
  // Fetch new data each time a new sample is selected
  buildCharts(newState);
  buildStatedata(newState);
}

// Initialize the dashboard
init();
