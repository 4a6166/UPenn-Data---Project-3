let searchInput = document.getElementById("schoolSearch");
let searchString = '';

searchInput.addEventListener('input', function (event) {
    searchString = searchInput.value.toLowerCase();
    if (event.key === 'Enter') {
        let matchingSchools = Object.keys(radarChartData).filter(schoolKey => schoolKey.toLowerCase().includes(searchString));
        if (matchingSchools.length === 1) {
            radarChart(radarChartData, matchingSchools[0]);
            gaugeChart(matchingSchools[0]);
        } else {
            let defaultSchoolKey = Object.keys(radarChartData)[0];
            radarChart(radarChartData, defaultSchoolKey);
            gaugeChart(defaultSchoolKey);
        }
    }
});

searchInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        let matchingSchools = Object.keys(radarChartData).filter(schoolKey => schoolKey.toLowerCase().includes(searchString));
        if (matchingSchools.length === 1) {
            radarChart(radarChartData, matchingSchools[0]);
            gaugeChart(matchingSchools[0]);
        } else {
            let defaultSchoolKey = Object.keys(radarChartData)[0];
            radarChart(radarChartData, defaultSchoolKey);
            gaugeChart(defaultSchoolKey);
        }
    }
});
