import numpy as np
import os

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Home route
@app.route("/")
def welcome():

    return (
        f"<h1>Aloha, Welcome to Hawaii Weather Data</h1>"
        f"<h2>Available Routes:</h2>"
        f"<ul>"
        f"<li>/api/v1.0/precipitation</li>"
        f"<li>/api/v1.0/stations</li>"
        f"<li>/api/v1.0/tobs</li>"
        f"</ul>"
    )

@app.route('/api/v1.0/precipitation')
def precip():

    # setup a session for the query 
    # I'm using the same query from exploratory climate analysis, which gets 1 year of data, going backwards from the last date in the set
    session = Session(engine)

    # run a query to get the top 1 row of the data sorted by date desc.  (this gest the last date)
    results = session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1)

    # get the last data point, convert to datetime for later
    result = results[0]
    last_date = dt.datetime.strptime(result[0],'%Y-%m-%d')

    # get 1 year prior to last date
    last_year = last_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= last_year).all()

    # close the session to end the communication with the database
    session.close()

    # Create a dictionary from the row data and append to a list of the last year's precipitation
    all_precip = []
    for precip in results:
        precip_dict = {}
        precip_dict["date"] = precip.date
        precip_dict["prcp"] = precip.prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route('/api/v1.0/stations')
def stations():

    # setup a session
    session = Session(engine)

    # query for station data...
    results = session.query(Station).all()

    # close session
    session.close()

    # create a dicitonary of the station data and return as a json string
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict['id'] = station.id
        station_dict['station'] = station.station
        station_dict['name'] = station.name
        station_dict['latitude'] = station.latitude
        station_dict['longitude'] = station.longitude
        station_dict['elevation'] = station.elevation
        all_stations.append(station_dict)
    
    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def temps():

    # start the session
    session = Session(engine)

    # run a query to get the top 1 row of the data sorted by date desc.  (this gest the last date)
    results = session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1)

    # get the last data point, convert to datetime for later
    result = results[0]
    last_date = dt.datetime.strptime(result[0],'%Y-%m-%d')

    # get 1 year prior to last date
    last_year = last_date - dt.timedelta(days=365)
    
    # query for the temp data
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= last_year).all()

    # close session
    session.close()

    # create a dictionary of temp data and return as json
    all_temps = []
    for temp in results:
        temp_dict = {}
        temp_dict['station'] = temp.station
        temp_dict['date'] = temp.date
        temp_dict['tobs'] = temp.tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route('/api/v1.0/<start>')
def avg_temp_start(start):

    # start the session
    session = Session(engine)

    # query to get the avg
    results = session.query(Measurement.date, func.avg(Measurement.tobs).label('Avg_Temp'), func.min(Measurement.tobs).label('Low_Temp'), func.max(Measurement.tobs).label('High_Temp')).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    
    session.close()

    all_data = []
    for temp in results:
        temp_dict = {}
        temp_dict['date'] = temp.date
        temp_dict['Avg Temp'] = temp.Avg_Temp
        temp_dict['Low Temp'] = temp.Low_Temp
        temp_dict['Hight Temp'] = temp.High_Temp
        all_data.append(temp_dict)
    
    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True)