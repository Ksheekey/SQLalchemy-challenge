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

#earliest_date = date_id_first
#latest_date  = date_id_last


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
    #ALL = session.query(M,S).filter(M.station == S.station).all()
    results = session.query(S.name).all()
    session.close()
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

###----------------------------------------------------------------
##Query the dates and temperature observations of the most active station for the last year of data.
##Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def Tobs():
    session = Session(engine)
    #ALL = session.query(M,S).outerjoin(M.station == S.station).all()
    station_activity = session.query(M.station, func.count(M.station)).group_by(M.station).order_by(func.count(M.station).desc()).limit(1).all()
    station_act = list(np.ravel(station_activity))
    station_id = station_act[0]

    date_activity = session.query(M.date).order_by((M.date).desc()).limit(1).all()
    date_act = list(np.ravel(date_activity))
    date_id = date_act[0]
    #date_id = 2017-08-23

    last_yr_date = '2016-08-23'
    tobs_info = session.query(M.tobs).filter(S.station == station_id).filter(M.date >= last_yr_date).all()
    all_tobs = list(np.ravel(tobs_info))
    session.close

    return jsonify(all_tobs)

###----------------------------------------------------------------
##Return a JSON list of the minimum temperature, the average temperature, 
#   and the max temperature for a given start or start-end range.
##When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` 
#   for all dates greater than and equal to the start date.



@app.route("/api/v1.0/<start>")
def start_only(start):
    session = Session(engine)
    date_activity_start = session.query(M.date).all()
    date_act_start = list(np.ravel(date_activity_start))

    for date in date_activity_start:
        search_term = date['start'].lower()

    x = session.query(M.date).filter(M.date >= search_term).all()
    x_list = list(np.ravel(x))
    return jsonify(x_list)

    #return jsonify(date_act_start), 404


###----------------------------------------------------------------  
##When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
#   for dates between the start and end date inclusive.   

#@app.route("/api/v1.0/<start>/<end>")
#def start_end():

###----------------------------------------------------------------

# homepage
@app.route("/")
def home():
    session = Session(engine)
    date_activity_first = session.query(M.date).order_by((M.date).asc()).limit(1).all()
    date_activity_last = session.query(M.date).order_by((M.date).desc()).limit(1).all()
    date_act_first = list(np.ravel(date_activity_first))
    date_act_last = list(np.ravel(date_activity_last))
    date_id_first = date_act_first[0]
    date_id_last = date_act_last[0]
    return (
        f"Welcome to Climate Analysis and Exploration<br>"
        "<br>"
        f"for precipitation info type the following onto the end of the task bar:<br>"
        f"/api/v1.0/precipitation <br>"
        "<br>"
        f"for station info type type the following onto the end of the task bar:<br>"
        f"/api/v1.0/stations <br>"
        "<br>"
        f"for temperature info type the following onto the end of the task bar:<br>"
        f"/api/v1.0/tobs <br>"
        "<br>"
        f"for temperature info starting on a certain date type the following onto the end of the task bar (earliest date is {date_id_first}):<br>"
        f" /api/v1.0/<start> <br>"
        "<br>"
        f"for temperature info between two dates type the following onto the end of the task bar (earliest date is {date_id_first}, latest date is {date_id_last}):<br>"
        f" /api/v1.0/<start>/<end>"
        f"<br>"
        f"<br>"
        f"<br>"
        f"<br>"
        f"<br>"
        f"<br>"
        f"<br>"
        f"<br>"
        f"<br>"
        f"<br>"
        f"By: Kevin Sheekey"
    )
   

if __name__ == "__main__":
    app.run(debug=True)    