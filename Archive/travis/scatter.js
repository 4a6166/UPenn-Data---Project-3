// Default View is Totals vs alg
// Alternatively we can do Totals vs bio and Totals vs lit



let total = getTotals()


function getTotals(){
    return [1, 2, 3, 4]    
}


function plotSelectedProficiencies(fieldName) {
  let subjectData = []
  if (fieldName === 'alg') subjectData = [1, 2, 3, 4]
  if (fieldName === 'bio') subjectData = [2, 4, 6, 8]
  if (fieldName === 'lit') subjectData = [1, 2, 3, 4]

  var data = {
    x: total,
    y: subjectData,
    mode: 'markers',
    type: 'scatter'
  };
  
  Plotly.newPlot('scatter-plot', [data]);
}



plotSelectedProficiencies('alg')

 
