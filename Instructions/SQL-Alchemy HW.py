#SQL-Alchemy HW

from datetime import datetime

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
def tobs():
    session = Session(engine)
    #ALL = session.query(M,S).outerjoin(M.station == S.station).all()
    station_activity = session.query(M.station, func.count(M.station)).group_by(M.station).order_by(func.count(M.station).desc()).limit(1).all()
    station_act = list(np.ravel(station_activity))
    station_id = station_act[0]

    date_activity = session.query(M.date, M.tobs).order_by((M.date).desc()).limit(1).all()
    date_act = list(np.ravel(date_activity))
    date_id = date_act[0]
    date_id_dt = datetime.strptime(date_id, '%Y-%m-%d')
    just_month = date_id_dt.month
    format_month = '{:02d}'.format(just_month)
    last_yr_date = (f"{date_id_dt.year -1}-0{format_month}-{date_id_dt.day}")
    
    tobs_info = session.query(M.date, M.tobs).filter(S.station == station_id).filter(M.date >= last_yr_date).all()
    session.close

    date_tobs = []
    for date, tobs in tobs_info:
        datob_dict = {}
        datob_dict["date"] = date
        datob_dict["tobs"] = tobs
        date_tobs.append(datob_dict)

    return jsonify(date_tobs)

###----------------------------------------------------------------
##Return a JSON list of the minimum temperature, the average temperature, 
#   and the max temperature for a given start or start-end range.
##When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` 
#   for all dates greater than and equal to the start date.


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    Mdates = session.query(M.date).all()
    MMdates = list(np.ravel(Mdates))
    MMlist = []
    for date in MMdates:
        MMlist.append(date)

    canonicalized = start
    for date in MMlist:
        search_term = date

        if search_term == canonicalized:
            avgtemp = session.query(func.avg(M.tobs)).filter(M.date >= search_term).all()
            maxtemp = session.query(func.max(M.tobs)).filter(M.date >= search_term).all()
            mintemp = session.query(func.min(M.tobs)).filter(M.date >= search_term).all()

            for temp in avgtemp:
                avg = temp

            for temp_ave in avg:
                average_temp = temp_ave

            for mxtemp in maxtemp:
                maxt = mxtemp

            for temp_max in maxt:
                maximum_temp = temp_max
                
            for mntemp in mintemp:
                mint = mntemp

            for temp_min in mint:
                minimum_temp = temp_min

            session = Session(engine)
            date_activity_last = session.query(M.date).order_by((M.date).desc()).limit(1).all()
            date_act_last = list(np.ravel(date_activity_last))
            date_id_last = date_act_last[0]

            return (
                    f"The average temp between {start} and {date_id_last} was {average_temp}"
                    f"<br>"
                    f"<br>"
                    f"The maximum temp between {start} and {date_id_last} was {maximum_temp}"
                    f"<br>"
                    f"<br>"
                    f"The minimum temp between {start} and {date_id_last} was {minimum_temp}"
                    )

    return jsonify("YOU STINK PAL, TRY AGAIN")

    
###----------------------------------------------------------------  
##When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
#   for dates between the start and end date inclusive.   

@app.route("/api/v1.0/<tart>/<end>")
def date_tart(tart,end):
    session = Session(engine)
    Mdates = session.query(M.date).all()
    MMdates = list(np.ravel(Mdates))
    MMlist = []
    #EElist = []
    for dates in MMdates:
        MMlist.append(dates)
        #EElist.append(dates)

    canonicalized = end
    for date in MMlist:
        search_term = date

        if search_term == canonicalized:
            abc_avgtemp = session.query(func.avg(M.tobs)).filter(M.date <= search_term).all()
            abc_maxtemp = session.query(func.max(M.tobs)).filter(M.date <= search_term).all()
            abc_mintemp = session.query(func.min(M.tobs)).filter(M.date <= search_term).all()

            for abc_temp in abc_avgtemp:
                abc_avg = abc_temp

            for abc_temp_ave in abc_avg:
                abc_average_temp = abc_temp_ave

            for abc_mxtemp in abc_maxtemp:
                abc_maxt = abc_mxtemp

            for abc_temp_max in abc_maxt:
                abc_maximum_temp = abc_temp_max
                
            for abc_mntemp in abc_mintemp:
                abc_mint = abc_mntemp

            for abc_temp_min in abc_mint:
                abc_minimum_temp = abc_temp_min


            return (
                    f"The average temp between the dates given was {abc_average_temp}"
                    f"<br>"
                    f"<br>"
                    f"The maximum temp between the dates given was {abc_maximum_temp}"
                    f"<br>"
                    f"<br>"
                    f"The minimum temp between the dates given was {abc_minimum_temp}"
                    )

    return jsonify("YOU STINK PAL, TRY AGAIN"), 404
 
 
###----------------------------------------------------------------
@app.route("/api/v1.0/kevin")
def kevin():
    session = Session(engine)
    date_activity = session.query(M.date, M.tobs).order_by((M.date).desc()).limit(1).all()
    date_act = list(np.ravel(date_activity))
    date_id = date_act[0]
    date_id_dt = datetime.strptime(date_id, '%Y-%m-%d')
    just_month = date_id_dt.month
    format_month = '{:02d}'.format(just_month)
    last_yr_date = (f"{date_id_dt.year -1}-{format_month}-{date_id_dt.day}")
    return (f"{last_yr_date}" )
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
    station_activity = session.query(M.station, func.count(M.station)).group_by(M.station).order_by(func.count(M.station).desc()).limit(1).all()
    station_act = list(np.ravel(station_activity))
    station_id = station_act[0]
    return (
        f"Welcome to Climate Analysis and Exploration<br>"
        f"(earliest date is {date_id_first}, latest date is {date_id_last})<br>"
        "<br>"
        f"for precipitation info type the following onto the end of the task bar:<br>"
        f"/api/v1.0/precipitation <br>"
        "<br>"
        f"for station info type type the following onto the end of the task bar:<br>"
        f"/api/v1.0/stations <br>"
        "<br>"
        f"for temperature info for the busiest station ({station_id}) type the following onto the end of the task bar:<br>"
        f"/api/v1.0/tobs <br>"
        "<br>"
        f"for temperature info starting on a certain date type the following onto the end of the task bar then the date requested. (example /api/v1.0/2012-07-12):<br>"
        f" /api/v1.0/<start> <br>"
        "<br>"
        f"for temperature info between two dates type the following onto the end of the task bar then the date requested. (example /api/v1.0/2013-04-29/2014-11-06):<br>"
        f" /api/v1.0/<start>/<end> <br>"
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