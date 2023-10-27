// Set the relative file path here.
var filePath = '../Resources/Output/keystone_expenditure.json';

let radarChartData = {};
let gaugeChartData = {};
let allPerPupilExpenditureData = [];

d3.json(filePath).then((data) => {
    data.forEach((item) => {
        let schoolName = item['School Name'];
        let districtName = item['District Name'];
        let subject = item['Subject'];
        let percentAP = item['Percent Advanced & Proficient'];
        let perPupilExpenditure = item['2018-2019 Local Per Pupil Expenditure'];
        let schoolKey = getUniqueSchoolKey(schoolName, districtName);

        if (!radarChartData[schoolKey]) {
            radarChartData[schoolKey] = {
                labels: [],
                data: [],
            };
        }

        if (!radarChartData[schoolKey].labels.includes(subject)) {
            radarChartData[schoolKey].labels.push(subject);
        }

        radarChartData[schoolKey].data.push(percentAP);

        if (!gaugeChartData[schoolKey]) {
            gaugeChartData[schoolKey] = {
                data: []
            };
        }
        gaugeChartData[schoolKey].data.push(perPupilExpenditure);
        allPerPupilExpenditureData.push(perPupilExpenditure);
    });

    let maxPerPupilExpenditure = Math.max(...allPerPupilExpenditureData);

    // Set the initial school keys for radar and gauge charts
    let radar_sample = Object.keys(radarChartData)[0];
    let gauge_sample = Object.keys(gaugeChartData)[0];

    // Call the functions to initialize radar and gauge charts
    radarChart(radarChartData, radar_sample);
    gaugeChart(gauge_sample, maxPerPupilExpenditure);
});

// Function to create a unique school-district name pair.
function getUniqueSchoolKey(schoolName, districtName) {
    return `${schoolName}-${districtName}`;
};

// Function to create and update the radar chart.
function radarChart(radarChartData, radar_sample) {
    const CHART = document.getElementById('myRadarChart');
    CHART.width = 600;
    CHART.height = 600;
    Chart.defaults.scale.ticks.beginAtZero = true;

    let Trace = new Chart (CHART, {
        type: 'radar',
        data: {
            labels: ['Algebra 1', 'Biology', 'Literature'],
            datasets: [
                {
                    label: radar_sample,
                    data: radarChartData[radar_sample].data,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)'
                }
            ]
        },
        options: {
            scale: {
                ticks: {
                    min: 0,
                    max: 100,
                    stepSize: 10
                }
            }
        }
    });
};

// Function to create and update the gauge chart. 
function gaugeChart(gauge_sample, maxPerPupilExpenditure) {
    let perPupilExpenditureData = gaugeChartData[gauge_sample].data;
    let dataTrace = [{
        domain: {x: [0,1], y: [0,1]},
        mode: 'gauge+number',
        value: perPupilExpenditureData[0],
        title: {
            text: `<b>${gauge_sample}</b><br>${'Per Pupil Expenditure USD'}</br>`,
            font: {color: 'black', size: 18}
        },
        type: 'indicator',
        gauge: {
            axis: {
                range: [0, maxPerPupilExpenditure],
            },
            steps: [
                { range: [0, 10000], color: 'lightgray' },
                { range: [10000, 30000], color: 'rgb(255, 230, 230)' },
                { range: [30000, 50000], color: 'rgb(255, 179, 179)' },
                { range: [50000, 70000], color: 'rgb(255, 128, 128)' },
                { range: [70000, 90000], color: 'rgb(255, 77, 77)' },
                { range: [90000, 100000], color: 'rgb(255, 26, 26)' },
            ]
        }
    }];
    Plotly.newPlot('gaugeChart', dataTrace);
}
