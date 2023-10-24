// Load the Top 25 data
// let finalRank = "../Katy/compare_ranks.json";

// d3.json(finalRank).then(function(data) {
//     console.log(data)
// });

// let data = [{district: "District Name", rank: "Rank", value: "Value Ranking"}]; 

// JS 
let chart, palette = ['#1b4289', '#d0d0d0']; 
let selectEl; 

console.log(data);
// let leftCategories = JSC.sortBy(data, 'Rank') 
//     .reverse() 
//     .map(function(v) { 
//       return v.district; 
//     }), 
//   rightCategories = JSC.sortBy(data, 'Value Ranking') 
//     .reverse() 
//     .map(function(v) { 
//       return v.district; 
//     }); 
  
// let series = getSeries(data); 
// bindUi(); 
// populateDropdown(series); 
  
// chart = JSC.Chart( 
//   'chart', 
//   { 
//     debug: true, 
//     animation_duration: 0, 
//     chartArea_clipContent: false, 
//     legend_visible: false, 
//     yAxis: { 
//       visible: false, 
//       formatString: 'n0', 
//       scale: { 
//         range: [ 
//           -0.5, 
//           leftCategories.length - 0.5 
//         ], 
//         invert: true
//       } 
//     }, 
//     xAxis: { 
//       scale_range_padding: 1.2, 
//       defaultTick: { 
//         label: { maxWidth: 60, color: '#9E9E9E' }, 
//         gridLine: { 
//           visible: false, 
//           center: true
//         }, 
//         line_color: 'none'
//       }, 
//       scale: { range: { min: -0.7, max: 1.3 } } 
//     }, 
//     defaultTooltip_enabled: false, 
//     defaultSeries: { 
//       opacity: 0.1, 
//       states: { 
//         select: { opacity: 1, color: palette[0] }, 
//         hover_enabled: false, 
//         mute_enabled: false
//       }, 
//       firstPoint_label: { 
//         text: 
//           '%seriesName <b>%zValue</b> ({%yValue+1})', 
//         align: 'left'
//       }, 
//       lastPoint_label: { 
//         text: '<b>%zValue</b> ({%yValue+1})', 
//         align: 'right'
//       }, 
//       events: { 
//         mouseOver: function() { 
//           var id = this.options('name'); 
//           dropdownSelect(id); 
//           highlightSeries(id); 
//           return false; 
//         } 
//       } 
//     }, 
//     defaultPoint: { 
//       label: { 
//         color: '%color', 
//         verticalAlign: 'middle'
//       }, 
//       marker: { 
//         type: 'circle', 
//         outline_width: 0, 
//         size: 12 
//       }, 
//       states: { 
//         hover_enabled: false, 
//         mute_enabled: false
//       }, 
//       focusGlow: false
//     }, 
//     series: series 
//   }, 
//   function(c) { 
//     chart = c; 
//     dropdownSelect('RADNOR TOWNSHIP SD'); 
//     highlightSeries('RADNOR TOWNSHIP SD'); 
//   } 
// ); 
  
// function getSeries(districtData) { 
//   return districtData.map(function(v) { 
//     var district = v.district; 
//     (leftI = leftCategories.indexOf(district)), 
//       (rightI = rightCategories.indexOf(district)); 
//     return { 
//       name: district, 
//       color: palette[1], 
//       points: [ 
//         { 
//           x: 'Rank', 
//           y: leftI, 
//           z: v['Rank'] 
//         }, 
//         { 
//           x: 'Value Ranking', 
//           y: rightI, 
//           z: v['Value Ranking'] 
//         } 
//       ] 
//     }; 
//   }); 
// } 
  
// function highlightSeries(id) { 
//   /* Unselect any selected series */
//   chart 
//     .series(function(s) { 
//       return s.options('selected'); 
//     }) 
//     .options( 
//       { 
//         selected: false, 
//         defaultPoint_label_color: palette[1] 
//       }, 
//       false
//     ); 
  
//   /* Select series with given ID */
//   chart 
//     .series(id) 
//     .options({ 
//       selected: true, 
//       defaultPoint_label_color: palette[0] 
//     }); 
// } 
  
// function bindUi() { 
//   selectEl = document.getElementById( 
//     'selectDistrict'
//   ); 
//   selectEl.addEventListener('change', function() { 
//     selectChanged(this); 
//   }); 
  
//   function selectChanged(control) { 
//     highlightSeries( 
//       control.options[control.selectedIndex].value 
//     ); 
//   } 
// } 
  
// function dropdownSelect(id) { 
//   for ( 
//     var i = 0; 
//     i < selectEl.options.length; 
//     i++ 
//   ) { 
//     if (selectEl.options[i].text === id) { 
//       selectEl.options[i].selected = true; 
//       return; 
//     } 
//   } 
// } 
  
// function populateDropdown(series) { 
//   series.forEach(function(s) { 
//     var el = document.createElement('option'); 
//     el.textContent = s.name; 
//     el.value = s.name; 
//     selectEl.appendChild(el); 
//   }); 
// } 