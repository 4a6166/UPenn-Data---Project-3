

let total = getTotals()


function getTotals(){
    // d3.json('urlfortotals')
    return [1, 2, 3, 4]    
}


function plotSelectedProficiencies(fieldName) {
  let subjectData = []
  if (fieldName === 'alg') subjectData = [1, 2, 3, 4]
  if (fieldName === 'bio') subjectData = [2, 4, 6, 8]
  if (fieldName === 'lit') subjectData = [.1, .2, .3, .4]

  // if (fieldName === 'alg') subjectData = d3.json('urlforalg')
  // if (fieldName === 'bio') subjectData = d3.json('urlforbio')
  // if (fieldName === 'lit') subjectData = d3.json('urlforlit')

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

 
