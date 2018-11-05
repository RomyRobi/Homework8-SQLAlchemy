
# coding: utf-8

# In[9]:


import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt
import pandas as pd


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# In[10]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results
# Latest Date
latest = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# Calculate the date 1 year ago from today
year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
# Perform a query to retrieve the data and precipitation scores
precip_data = session.query(Measurement.date, Measurement.prcp).    filter(Measurement.date > year_ago).all()


# In[11]:


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    """Query for the dates and temperature observations from the last year.
Convert the query results to a Dictionary using date as the key and tobs as the value.
Return the JSON representation of your dictionary."""
    precip_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > year_ago).all()
    precip_dict = {}
    for data in precip_data:
         precip_dict[data[0]] = data[1]
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return json list of stations from data set."""
    station_data = session.query(Measurement.date, Measurement.prcp, Measurement.station, Measurement.tobs).\
    filter(Measurement.date > year_ago).all()
    station_data_df = pd.DataFrame(station_data)
    station_data_df = station_data_df.set_index("date")
    stations = station_data_df["station"].unique()
    station_dict = {"Station Names": list(stations)}
    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    temp_station = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > year_ago).all()
    temp_dict = {}
    for data in temp_station:
        temp_dict[data[0]] = data[1]
    return jsonify(temp_dict)



if __name__ == '__main__':
    app.run(debug=True)
