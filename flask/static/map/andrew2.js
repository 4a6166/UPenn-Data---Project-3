// Creating the map object
let myMap = L.map("chart", {
    center: [41, -77.5],
    zoom: 7.5
  });
  
  // Adding the tile layer
  // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  // }).addTo(myMap);
  
  // Load the GeoJSON data.
  let geoData = data
  let d1
  
  // Get the data with d3.
d3.json("/api/map?view=lit").then( (d) => {
    d1 = d
    
    let valueProperty = "pupil_expend"; // Default valueProperty
    let geojson; // Define geojson globally
    let scale;
    let legend;
  
    // Function to update the choropleth layer with the selected valueProperty
    function updateMap(valueProp) {
      if (geojson) {
        myMap.removeLayer(geojson);
      }
      if (legend) {
        myMap.removeControl(legend);
      }

      if (valueProp === "pupil_expend") {
        scale = ["#f7fcf5", "#00441b"]; // Scale for pupil_expend
      } else if (valueProp === "algebra") {
        scale = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]; // Scale for algebra
      } else if (valueProp === "literature") {
        scale = ["#edf8fb", "#b3cde3", "#8c96c6", "#8856a7", "#810f7c"]; // Scale for literature
      } else if (valueProp === "biology") {
        scale = ["#ffffcc", "#c2e699", "#78c679", "#31a354", "#006837"]; // Scale for biology
      }
  
      geojson = L.choropleth(data, {
        valueProperty: valueProp,
        scale: scale,
        steps: 20,
        mode: "q",
        style: {
          color: "#fff",
          weight: 1,
          fillOpacity: 0.8
        },
        onEachFeature: function(feature, layer) {
          layer.bindPopup('<h2>' + feature.properties.school_dis + '</h2> <strong>Per Pupil Expenditure 2018-19:</strong> $' +
          feature.properties.pupil_expend + '<br />' + '<strong>Algebra Proficiency: </strong>' + feature.properties.algebra +
          '%' + '<br />' + '<strong>Literature Proficiency: </strong>' + feature.properties.literature + '%' + '<br />' +
          '<strong>Biology Proficiency: </strong>' + feature.properties.biology + '%');
        }
      }).addTo(myMap);

      updateLegend(geojson, valueProp, scale);
    }
  
      // Set up the legend.
    function updateLegend(geojson, valueProp, scale) {
        legend = L.control({ position: "bottomright" });
        legend.onAdd = function() {
          let div = L.DomUtil.create("div", "info legend");
          let limits = geojson.options.limits;
          let colors = geojson.options.colors;
          let labels = [];
      
          let legendTitle;
          if (valueProp === "pupil_expend") {
            legendTitle = "Per Pupil Expenditure"; // Legend title for pupil_expend
          } else if (valueProp === "algebra") {
            legendTitle = "Percent Proficient in Algebra"; // Legend title for algebra
          } else if (valueProp === "literature") {
            legendTitle = "Percent Proficient in Literature"; // Legend title for literature
          } else if (valueProp === "biology") {
            legendTitle = "Percent Proficient in Biology"; // Legend title for biology
          }
  
          // Add the legend heading and minimum and maximum.
          let legendInfo = "<h1>" + legendTitle + "</h1>" +
          "<div class=\"labels\">" +
          "<div class=\"min\">" + limits[0] + "</div>" +
          "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
          "</div>";
  
          div.innerHTML = legendInfo;
  
          limits.forEach(function(limit, index) {
            labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
          });
  
        div.innerHTML += "<ul>" + labels.join("") + "</ul>";
        return div;
      };
  
      // Adding the legend to the map
      legend.addTo(myMap);
    }
  
    // Dropdown change event listener
    let radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach((radio) => {
      radio.addEventListener("change", function () {
        valueProperty = this.id;
        updateMap(valueProperty);
      });
    });
  
    // Initial map generation
    updateMap(valueProperty);
})

// pseudocode
// for aun in geojson
//    for jaun in json
//      if aun == jaun
//          goejson[proficient] == json[proficient]
