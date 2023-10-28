// refactor of andrew2.js to use APIs
// create map
let myMap = L.map("chart", {
  center: [41, -77.5],
  zoom: 7.5
});
  
// bind controls
let radioButtons = document.querySelectorAll('input[type="radio"]');
radioButtons.forEach((radio) => {
  radio.addEventListener("change", function () {
    valueProperty = this.id;
    console.log(valueProperty)
    updateMap(valueProperty);
  });
})

// update legend
let updateLegend = (geojson, view) => {
  legend = L.control({ position: "bottomright" });
  legend.onAdd = function() {
    let div = L.DomUtil.create("div", "info legend");
    let limits = geojson.options.limits;
    let colors = geojson.options.colors;
    let labels = [];

    let legendTitle;
    if (view === "pupil") {
      legendTitle = "Per Pupil Expenditure"; // Legend title for pupil_expend
    } else if (view === "alg") {
      legendTitle = "Percent Proficient in Algebra"; // Legend title for algebra
    } else if (view === "lit") {
      legendTitle = "Percent Proficient in Literature"; // Legend title for literature
    } else if (view === "bio") {
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

// pair imported geojson (data var) to view from api
let pairGeoJSON = (d, geojson) => {
  console.log("pairing...")
  // deep copy of geojson for modification
  let g = JSON.parse(JSON.stringify(geojson))
  col = "Total"

  for (feature of g.features){
    // geojson file has aun_num (doesn't match) and aun_schdis (matches)
    let AUN_g = parseInt(feature.properties.aun_schdis)
    for (row of d){
      let AUN_d = parseInt(row.AUN);
      if(AUN_g == AUN_d){
        feature.properties['choro_val'] = row[col];
        feature.properties['choro_val'] = row[col];
        break;
      } 

      feature.properties['pupil_expend'] = null;
      feature.properties['choro_val'] = null;
    }
  }
  
  return g;
}

// d3
let updateMap = (view) => {
  d3.json("/api/map?view=" + view).then( d => {
    // clear vis
    myMap.eachLayer( (layer) => {
      myMap.removeLayer(layer)
    })
    try {
    myMap.removeControl(legend)
    } catch (error) {
      console.log("https://i.kym-cdn.com/entries/icons/original/000/027/763/07B89120-B48D-45FB-AF1D-49AF6CD16790.jpeg")
    }
    
    // pair geojson
    let geojson = pairGeoJSON(d, data);
    
    //set scale
    if (view === "pupil") {
        scale = ["#f7fcf5", "#00441b"]; // Scale for pupil_expend
      } else if (view === "alg") {
        scale = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]; // Scale for algebra
      } else if (view === "lit") {
        scale = ["#edf8fb", "#b3cde3", "#8c96c6", "#8856a7", "#810f7c"]; // Scale for literature
      } else if (view === "bio") {
        scale = ["#ffffcc", "#c2e699", "#78c679", "#31a354", "#006837"]; // Scale for biology
      }

    
    // create choropleth and add to map
    let choropleth = L.choropleth(geojson, {
      valueProperty: 'choro_val',
      scale: scale,
      steps: 20,
      mode: "q",
      style: {
        color: "#fff",
        weight: 1,
        fillOpacity: 0.8
      },
      onEachFeature: function(feature, layer) {
        layer.bindPopup(`
          <h2>${feature.properties.school_dis}</h2>
          <strong>${view} 2018-2019: </strong> ${Math.round(feature.properties.choro_val*100)/100}
          `)
        // layer.bindPopup('<h2>' + feature.properties.school_dis + '</h2> <strong>Per Pupil Expenditure 2018-19:</strong> $' +
        //   feature.properties.pupil_expend + '<br />' + '<strong>Algebra Proficiency: </strong>' + feature.properties.algebra +
        //   '%' + '<br />' + '<strong>Literature Proficiency: </strong>' + feature.properties.literature + '%' + '<br />' +
        //   '<strong>Biology Proficiency: </strong>' + feature.properties.biology + '%');
      }
    }).addTo(myMap);


    // add legend
    updateLegend(choropleth, view)
  })
}

// inital map data setup
updateMap("pupil")
