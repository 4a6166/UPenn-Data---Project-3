
let total = getTotals()


function getTotals(){
    d3.json('/api/scatter/pupil').then( (d) => {
      return d    
    })
}


function plotSelectedProficiencies(fieldName) {
  let subjectData = []
  if (fieldName === 'alg') subjectData = d3.json('/api/scatter?view=keystone_algebra')
  if (fieldName === 'bio') subjectData = d3.json('/api/scatter?view=keystone_biology')
  if (fieldName === 'lit') subjectData = d3.json('/api/scatter?view=keystone_literature')

  var data = {
    x: total,
    y: subjectData,
    mode: 'markers',
    type: 'scatter'
  };
  
  Plotly.newPlot('chart', [data]);
  console.log('asdf')
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
