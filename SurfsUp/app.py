# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
import sqlalchemy.orm
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# connect to the database
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save refrences to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to theDB
session = Session(engine)

#################################################
# Flask Routes
#################################################
# home route
@app.route("/")
def home():
    return(
        f"<center><h2>Welcome to the Hawaii Climate Analysis Local API!</h2></center>"
        f"<center><h3>select from one of the available routes:</h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/station</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/start/end</center>"
    )

# /api/v1.0/percipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    # return the previous year's percipitaion as a json
    # Calculate the date one year from the last date in data set.
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    # Perform a query to retrive the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previous_year).all()
    
    session.close()
    #dictionary with the date as the key and percipitation (prcp) as the value 
    percipitation = {date: prcp for date, prcp in results}

    # convert to a json
    return jsonify(percipitation)

# /api/v1.0/stations route
@app.route("/api/v1.0/stations") 
def stations():
    # show a list of stations
    # Perform a query to retrieve the name of the stations
    results = session.query(station.station).all()
    session.close()

    station_list = list(np.ravel(results))

    # convert to a json and display
    return jsonify(station_list)

# /api/v1.0/tobs route 
@app.route("/api/v1.0/tobs") 
def temperatures():
    # return the previous year tempratures
    # Calculate the date one year from the last date in data set.
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    #previousYear

    # Perform a query to retrive the temperatures from most active station from the past year
    results = session.query(measurement.tobs).\
            filter(measurement.station == 'USC00519281').\
            filter(measurement.date >= previous_year).all()
    session.close()

    temperature_list = list(np.ravel(results))

    # return the list of temperatures
    return jsonify(temperature_list)

# /api/v1.0/start/end and /api/v1.0/start routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):
    # select statement
    selection = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

    if not end:
        start_date = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(measurement.date >= start_date).all()

        session.close()

        temperature_list = list(np.ravel(results))

        # return the list of temperatures
        return jsonify(temperature_list)
    
    else:
        start_date = dt.datetime.strptime(start, "%m%d%Y")
        end_date = dt.datetime.strptime(end, "%m%d%Y")

        results = session.query(*selection)\
            .filter(measurement.date >= start_date)\
            .filter(measurement.date <= end_date).all()
        
        session.close()

        temperature_list = list(np.ravel(results))

        # return the list of temperatures
        return jsonify(temperature_list)
    

#################################################
# app launcher
#################################################
if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
