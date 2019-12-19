# sql-challenge
## by Michael Dowlin
### 12/17/19

![Alt text](/images/surfs-up.png)

#### Description
This project looks at Hawaii weather data in a sqllite database.  The tools used are Python and SQLAlchemy.  The Jupyter notebook "climate.ipynb" does the exploration and analysis of the weather data.  The charts generated by the analysis are contained in the images folder.  The python file "app.py" will launch a flask application that will act as a api on the local machine.  The routes will lead to the different analysis results (data in json format).  Only part of the bonus is done, I'll come back later to attempt the rest!

#### Contents

| File                         | Description                                                                                     |
|------------------------------|-------------------------------------------------------------------------------------------------|
|app.py                        | Python flask application.  Launch this from the project folder and you can access the api from the local host (typically port 5000)
|climate.ipynb                 | Main Jupyter notebook.  Based off of the starter notebook, the project answers all of the homework questions and a little bit more.  (But not all of the bonus)
images\precipitation.png       | The first chart in the assignment, it represents the last 12 months of precipitation data that is in the database, which is from 8/23/2016 to 8/23/2017
images\station-histogram.png   | A historgram of temperature for the station with the most observations.  It represents the last 12 months of data for that station
images\temperature.png         | A bar chart of average temperature from the same data used in the histogram chart. 
