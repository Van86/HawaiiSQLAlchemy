# import dependencies 
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite"")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    twelve_months = session.query(*sel).\
    filter(Measurement.date > '2016-08-22').\
    order_by(Measurement.date).all()

    # Convert list of tuples into normal list
    prcpTotal = []
    for result in precip:
        prcpDict = {}
        prcpDict["date"] = precip[0]
        prcpDict["prcp"] = precip[1]
        prcpTotal.append(prcpDict)

    return jsonify(prcpTotal)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #Query all stations
    stationsList = session.query(Station.station).all()

    #Convert list of tuples into normal list
    allStations = list(np.ravel(stationsList))

    #Return a JSON list of stations from the dataset
    return jsonify(allStations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    #query for the dates and temperature observations from a year from the last data point.
    most_obs = session.query(Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == most_active).\
    order_by(Measurement.tobs).all()
    
    tempTotals = []
    for result in temp:
        tempDict = {}
        tempDict["date"] = temp[0]
        tempDict["tobs"] = temp[1]
        tempTotals.append(tempDict)

    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(tempTotals)


@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def ranges(start=None, end=None):
    session = Session(engine)
    #when given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    if end != None:
        tempS = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    else:
        tempS = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    #Convert list of tuples into normal list
    allTemps = list(np.ravel(tempS))

    #Return a JSON list of Temperatures
    return jsonify(allTemps)

if __name__ == '__main__':
    app.run(debug=False)
