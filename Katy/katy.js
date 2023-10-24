// Load the Top 25 data
let finalRank = "../Resources/compare_ranks.json";

// Load the data for our final rankings
let finalRank = "../Resources/final_rank.json"

// Get the data with d3
d3.json(topRank).then(function(data) {
    console.log(data)
});

d3.json(finalRank).then(function(data) {
    console.log(data)
});

// JS 
var chart, 
  palette = ['#1b4289', '#d0d0d0']; 
var selectEl; 
var data1 = [ {rank: "Rank", district: data.}
  
]; 
  
var leftCategories = JSC.sortBy(data, 'W_20_21') 
    .reverse() 
    .map(function(v) { 
      return v.team; 
    }), 
  rightCategories = JSC.sortBy(data, 'W_21_22') 
    .reverse() 
    .map(function(v) { 
      return v.team; 
    }); 
  
var series = getSeries(data); 
bindUi(); 
populateDropdown(series); 
  
chart = JSC.Chart( 
  'chartDiv1', 
  { 
    debug: true, 
    animation_duration: 0, 
    chartArea_clipContent: false, 
    legend_visible: false, 
    yAxis: { 
      visible: false, 
      formatString: 'n0', 
      scale: { 
        range: [ 
          -0.5, 
          leftCategories.length - 0.5 
        ], 
        invert: true
      } 
    }, 
    xAxis: { 
      scale_range_padding: 1.2, 
      defaultTick: { 
        label: { maxWidth: 60, color: '#9E9E9E' }, 
        gridLine: { 
          visible: false, 
          center: true
        }, 
        line_color: 'none'
      }, 
      scale: { range: { min: -0.7, max: 1.3 } } 
    }, 
    defaultTooltip_enabled: false, 
    defaultSeries: { 
      opacity: 0.1, 
      states: { 
        select: { opacity: 1, color: palette[0] }, 
        hover_enabled: false, 
        mute_enabled: false
      }, 
      firstPoint_label: { 
        text: 
          '%seriesName <b>%zValue</b> ({%yValue+1})', 
        align: 'left'
      }, 
      lastPoint_label: { 
        text: '<b>%zValue</b> ({%yValue+1})', 
        align: 'right'
      }, 
      events: { 
        mouseOver: function() { 
          var id = this.options('name'); 
          dropdownSelect(id); 
          highlightSeries(id); 
          return false; 
        } 
      } 
    }, 
    defaultPoint: { 
      label: { 
        color: '%color', 
        verticalAlign: 'middle'
      }, 
      marker: { 
        type: 'circle', 
        outline_width: 0, 
        size: 12 
      }, 
      states: { 
        hover_enabled: false, 
        mute_enabled: false
      }, 
      focusGlow: false
    }, 
    series: series 
  }, 
  function(c) { 
    chart = c; 
    dropdownSelect('Phoenix Suns'); 
    highlightSeries('Phoenix Suns'); 
  } 
); 
  
function getSeries(data) { 
  return data.map(function(v) { 
    var team = v.team; 
    (leftI = leftCategories.indexOf(team)), 
      (rightI = rightCategories.indexOf(team)); 
    return { 
      name: team, 
      color: palette[1], 
      points: [ 
        { 
          x: '2020-2021 Season', 
          y: leftI, 
          z: v['W_20_21'] 
        }, 
        { 
          x: '2021-2022 Season', 
          y: rightI, 
          z: v['W_21_22'] 
        } 
      ] 
    }; 
  }); 
} 
  
function highlightSeries(id) { 
  /* Unselect any selected series */
  chart 
    .series(function(s) { 
      return s.options('selected'); 
    }) 
    .options( 
      { 
        selected: false, 
        defaultPoint_label_color: palette[1] 
      }, 
      false
    ); 
  
  /* Select series with given ID */
  chart 
    .series(id) 
    .options({ 
      selected: true, 
      defaultPoint_label_color: palette[0] 
    }); 
} 
  
function bindUi() { 
  selectEl = document.getElementById( 
    'selectTeam'
  ); 
  selectEl.addEventListener('change', function() { 
    selectChanged(this); 
  }); 
  
  function selectChanged(control) { 
    highlightSeries( 
      control.options[control.selectedIndex].value 
    ); 
  } 
} 
  
function dropdownSelect(id) { 
  for ( 
    var i = 0; 
    i < selectEl.options.length; 
    i++ 
  ) { 
    if (selectEl.options[i].text === id) { 
      selectEl.options[i].selected = true; 
      return; 
    } 
  } 
} 
  
function populateDropdown(series) { 
  series.forEach(function(s) { 
    var el = document.createElement('option'); 
    el.textContent = s.name; 
    el.value = s.name; 
    selectEl.appendChild(el); 
  }); 
} 