
#importing Dependencies
from cProfile import run
import datetime as dt
import numpy as np
import pandas as pd


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#setup a database
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

#reflect the database
Base.prepare(engine, reflect=True)


#Create refrences 
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session 
session = Session(engine)


#Using the magic method to check file source 
import app

print("example __name__ = %s", __name__)

if __name__ == "__main__":
    print("example is being run directly.")
else:
    print("example is being imported")


#setup a Flask
app = Flask(__name__)

#define the welcome route
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

 # Create precipitation route
@app.route("/api/v1.0/precipitation")

# Create the precipitation() function
def precipitation():
	# Calculate the date one year ago from the most recent date
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	# Query: get date and precipitation for prev_year
	precipitation = session.query(Measurement.date,Measurement.prcp) .\
		filter(Measurement.date >= prev_year).all()
		
	# Create dictionary w/ jsonify()--format results into .JSON
	precip = {date: prcp for date, prcp in precipitation}
	return jsonify(precip)   

                #Station route
@app.route("/api/v1.0/stations")

def stations():
	results = session.query(Station.station).all()
	# Unravel results into one-dimensional array with:
		# `function np.ravel()`, `parameter = results`
	# Convert results array into a list with `list()`
	stations = list(np.ravel(results))
	return jsonify(stations=stations) 

# NOTE: `stations=stations` formats the list into JSON
# NOTE: Flask documentation: https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.jsonify

            #Monthly temp route

@app.route("/api/v1.0/tobs")

def temp_monthly():
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	results = session.query(Measurement.tobs).\
		filter(Measurement.station == 'USC00519281').\
		filter(Measurement.date >= prev_year).all()
	temps = list(np.ravel(results))
	return jsonify(temps=temps)


                    #Statistic Route
# Provide both start and end date routes:
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Add parameters to `stats()`: `start` and `end` parameters
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)