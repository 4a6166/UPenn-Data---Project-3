# PROJECT 3 – GROUP 1

## Collaborators:
Andrew Belfiglio, Katy Phillips, Shikha Patel, Jacob Field, Travis Guadamuz Ruth, Peter Matsui, Michelle Wiley

## Project Guidelines:
For Project 3, you will work with your group to tell a story using data visualizations. Here are the specific requirements:

1.	Your visualization must include a 
    -	Python Flask-powered API, 
        -	HTML/CSS, 
    -	JavaScript, and 
    -	at least one database (SQL, MongoDB, SQLite, etc.).
2.	Your project should fall into one of the following three tracks:
    -	A combination of web scraping and Leaflet or Plotly
    -	A dashboard page with multiple charts that update from the same data
    -	A server that performs multiple manipulations on data in a database prior to visualization (must be approved)
3.	Your project should include at least one JS library that we did not cover.
4.	Your project must be powered by a dataset with at least 100 records.
5.	Your project must include some level of user-driven interaction (e.g., menus, dropdowns, textboxes).
6.	Your final visualization should ideally include at least three views.

## Topic: 
Analyze department of education data for the state of PA to determine if the “achievement rate” is comparable to the expenditure per pupil. Drill down into the districts of interest and look at additional mitigating factors that could also affect success rate and spend (ex. tax/income base, median household income, geographic considerations, student population)

Possible Questions to Consider:
- How can achievement be quantified? Statewide testing data  - High School reading and math? Standardized test scores? Graduation rates?
- Are there areas where expenditure may be more but achievement rate lower?
- Do IEP and ESL achievement rates follow the same path as standard classes in schools/districts?
- Does the number of students or number of students per teacher play a role in achievement status or expenditure per pupil?
- Assumption: Spend is the same across all grades per pupil if budget is not broken down by school level.
- Why should everyone in the state care about educational achievements and expenditure?

## Project Outline and Roles:
1.	Choose Topic - Group Effort
2.	Gather data - Shikha
3.	Create SQL Database - Michelle
4.	Link Database and Dashboard - Jacob
5.	Research/Try cluster data - Jacob
5.	Visual 1: Map - Andrew
6.	Visual 2: Scatter Plot - Travis
7.	Visual 3: Radar Chart - Peter
8.	Visual 4: Slope Graph - Katy
9.	Presentation

## Dashboard & Visualization Notes:
- Visual 1:
	- Map of school districts by funding and performance
	- Overlay the funding and subject scores to toggle between them
	- Possibility to drill down from total expenditure to high school expenditure
	- Possibility to review spend over entire course of school (K-12) per student
	- No real noticeable discrepancy between elementary, middle school, and high school in a single district
	- Possibility to bucket schools into small medium and large - by enrollment and spend
- Visual 2: 
	- Community Financials scatter plot
	- Looks at subject scores vs proportion of per pupil expenditure / median income rate / tax rate
	- Possibility to make points' size equivalent to district enrollment
- Visual 3:
	- Radar Chart of test scores on select schools
	- Define top schools in terms of scores 
	- Determine ideal shape of of chart
- Visual 4:
	- Slope Chart comparing our findings with the state rankings of school districts
- Underlying factors of performance to explore
	- Median Income
	- Taxes
	- Do taxes and income correlate are do some districts pay more taxes but have less income? Do these districts perform better/worse?
	- Geographic classification - Rural, Suburb, Town, City 


## Possible Data Resources:
- Department of Education - Data and Reporting
    - https://www.education.pa.gov/DataAndReporting/Pages/default.aspx
        - Enrollment Reports (2004-2023)
        - SAT Scores (2001-2019) and ACT Scores (2011-2019)
        - School Locale – “Urban/Rural” Classification of Schools and LEAs
- National Center for Education Statistics
    - https://nces.ed.gov/
        - Students per school district (2021-2023)
- School district boundaries:
    - https://data.pa.gov/Geospatial-Data/Pennsylvania-School-Districts-Boundaries/s629-r52w
- AFR Data: Summary Level Expenditure, revenue and tax information (2011-2022)
    - https://www.education.pa.gov/Teachers%20-%20Administrators/School%20Finances/Finances/AFR%20Data%20Summary/Pages/AFR-Data-Summary-Level.aspx
- Nation’s Report Card API
    - https://educationdata.urban.org/documentation/
- School District of Philadelphia
    - https://www.philasd.org/performance/programsservices/open-data/
- PA Dept of Community and Economic Development
    - https://munstats.pa.gov/Reports/ReportInformation2.aspx?report=CountyTaxSummary_Dyn_Excel
- Best School Districts in PA article 
    - https://patch.com/pennsylvania/across-pa/these-are-best-school-districts-pa-new-ranking-says

## Project Resources:
- Medium  - Flask Article
    - https://towardsdatascience.com/talking-to-python-from-javascript-flask-and-the-fetch-api-e0ef3573c451
- JavaScript Libraries
    - https://underscorejs.org/  - easier to manipulate data
    - https://lodash.com/ - data utility library
    - https://www.algolia.com/ - autofill addresses* (use for schools?)
    - https://www.chartjs.org/ - chart library
- Map subplots in Plotly
    - https://plotly.com/python/map-subplots-and-small-multiples/
- Pictorial charts 
    - https://www.highcharts.com/docs/chart-and-series-types/pictorial
- Slope Chart Example
    - http://www.npr.org/blogs/money/2014/05/20/313131559/how-far-your-paycheck-goes-in-356-u-s-cities

## Random Idea Tracker for Inspiration:
- Map based visualizations  - State  to District to Individual schools?
- Creates story – same type of graphs showing different views 
- Single source data
- Dashboard by year – dropdown menu
- Historical Graph Over Time
- Hover data of either spend or achievement over map of school district/county
- Could this information help influence policy makers?
- Cluster analysis wealth bands?
- Choropleth map by county or school district view 
- Markers in the county for the school district or summary statistics card if cannot segment by school district

Monday - 10/16 Notes
flask - week 10 similar outline
flask run
first - get db
second - routes to tree of html documents
default is home page - then buttons can host other pages or an API
dashboard - would be homepage - visuablizations would grab data from database loaded in 
app.py file 

python file using SQLAlchemy - pandas - push to database
SQLite viewer - view database 
SQLite and SQLAlchemy

pipeline - push through to JS variable
query result - pull in data . into visualization and data
flask lets you pass in data 

or create APIs - access like a normal API 
different api for each visualization 
API smaller buckets so not a full query - 

database start to try it out and then a full 
types of data to pull into visualization - query to pass through the API 

initial thought
test score data
per pupil expenditure
median income
tax info

homepage - what do we want people to know - how financilas/expenditures relate to performance?
first page - map page toggle through learner groups (std, iep, ill) and the metric (score, expenditure, etc)
second - scatter score vs expenditure - how related are they - 3 plots one each of score vs expenditure - 
    cluster chart - color changes or circles 

same page as a comparison - 
third - slope graph - explanation of rankings - compare to article 
fourth - radar chart - select their school district to drill down - individual school view

dropdown of multiple years if easy to download 
did COVID affect test scores and median income
start with 2019 data to have a complete year - 

statistical analysis - 
state average 

next buttons to force structure to data 

weighted averages for school test scores - peter - null values 
ELL - IEP - limited number of students they wont report subcategory bc of identity

consider school size?
proficienty percentage per subject - first map visual 

scatter plot - adjust for other mitigating factors like number of students, etc. 

define achievement - 
ROI - 
ratio of scores to spend 

add notes to the charts - self guided exploration of the data 
app / templates - html filled by flask as served / static - js and css
words added to HTML file 
header same for every website 
TAILWIND - css 
Bootstrap 

2020 spiked funding for COVID related stipends - possibility

scatter plot - expenditure vs median income 