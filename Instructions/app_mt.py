import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#Connect to Database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()

base.prepare(engine, reflect=True)

measurement = base.classes.measurement
station = base.classes.station
session = Session(engine)
#Connect flask 

app = Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii API for climate!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/Precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/Precipitation")
def precipitation():
    """The precipitation data for previous 12 months"""

    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previous_year).all()
    results_dict = {date: prcp for date, prcp in results}
    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    results = session.query(station.station).all()

    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous 12 months"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prev_year).all()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run()
