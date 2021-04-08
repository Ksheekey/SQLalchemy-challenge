#SQL-Alchemy HW

#51:09

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
M = Base.classes.measurement
S = Base.classes.station


# Flask Setup

# create app
app = Flask(__name__)

# homepage
@app.route("/")
def home():
    return (
        f"Welcome to the Home Page<br>"
        "<br>"
        f"for precipitation info type /api/v1.0/precipitation in the task bar<br>"
        "<br>"
        f"for stations info type /api/v1.0/stations in the task bar<br>"
        "<br>"
        f"for tobs info type /api/v1.0/tobs in the task bar<br>"
        "<br>"
        f"for tob info starting on a certain date type /api/v1.0/<start>"
        "<br>"
        f"for tob info between two dates type /api/v1.0/<start>/<end>"
    )

###----------------------------------------------------------------
##Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
##Return the JSON representation of your dictionary.


@app.route("/api/v1.0/precipitation")
def Precipitation():
    session = Session(engine)
    results = session.query(M.date, M.prcp).all()
    session.close()
    percip = []
    for date, prcp in results:
        percip_dict = {}
        percip_dict["date"] = date
        percip_dict["prcp"] = prcp
        percip.append(percip_dict)

    return jsonify(percip)

###----------------------------------------------------------------   
##Return a JSON list of stations from the dataset

@app.route("/api/v1.0/stations")
def Stations():
    session = Session(engine)
    results = session.query(S.station).all()
    session.close()
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

###----------------------------------------------------------------
##Query the dates and temperature observations of the most active station for the last year of data.
##Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def Tobs():
    session = Session(engine)
    #ALL = session.query(M,S).filter(M.station == S.station).all()
    station_activity = session.query(M.station, func.count(M.station)).group_by(M.station).order_by(func.count(M.station).desc()).limit(1).all()
    station_act = list(np.ravel(station_activity))
    station_id = station_act[0]

    date_activity = session.query(M.date).order_by((M.date).desc()).limit(1).all()
    date_act = list(np.ravel(date_activity))
    date_id = date_act[0]
    #date_id = 2017-08-23

    last_yr_date = '2016-08-23'
    tobs_info = session.query(M.tobs).filter(M.station == station_id).filter(M.date >= last_yr_date).all()
    all_tobs = list(np.ravel(tobs_info))
    session.close

    return jsonify(all_tobs)

###----------------------------------------------------------------
## `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
##Return a JSON list of the minimum temperature, the average temperature, 
#   and the max temperature for a given start or start-end range.
##When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` 
#   for all dates greater than and equal to the start date.
##When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
#   for dates between the start and end date inclusive. 

@app.route("/api/v1.0/<start>")
def start_only():

@app.route("/api/v1.0/<start>/<end>")
def start_end():

if __name__ == "__main__":
    app.run(debug=True)    