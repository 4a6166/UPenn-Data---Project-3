console.log("ScatterJS loaded")

// let total = getTotals()

let result
d3.json('/api/scatter?view=alg').then( (d) => {
  result = d
})

let total
d3.json('/api/pupil').then( (d2) => {
  total = d2
})

function plotSelectedProficiencies(view) {
  d3.json(`api/scatter?view=${view}`).then( (d) => { 
    var data = {
      x: total,
      y: d,
      mode: 'markers',
      type: 'scatter'
    };

    Plotly.newPlot('chart', [data]);
   })
}



// Dropdown change event listener
let radioButtons = document.querySelectorAll('input[type="radio"]');
radioButtons.forEach((radio) => {
  radio.addEventListener("change", function () {
    valueProperty = this.id;
    plotSelectedProficiencies(valueProperty);
  });
});


plotSelectedProficiencies('alg')

 
// =======
// const algebraContainer = document.getElementById('algebra')
// const bioContainer = document.getElementById('bio')
// const litContainer = document.getElementById('lit')
// algebraContainer.innerHTML={algebra} 
// bioContainer.innerHTML={bio} 
// litContainer.innerHTML={lit} 
// >>>>>>> Stashed changes
