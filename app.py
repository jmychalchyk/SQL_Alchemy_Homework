import numpy as np
import datetime as dt
import pandas as pd
from pandas import Series
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
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Mmt = Base.classes.measurement

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/Startdate/Enddate - format:<b>yyyy-mm-dd$$yyyy-mm-dd</b>"
    )


@app.route("/api/v1.0/precipitation")
def precep1():
    sel = [Mmt.prcp,Mmt.date]
    Precip = session.query(*sel).all()
    
    all_precip = []
    for days in Precip:
        precip_dict = {}
        precip_dict["Day"] = days[1]
        precip_dict["Precipitation"] = days[0]
        all_precip.append(precip_dict)

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations1():
 
    results = session.query(Mmt.station).group_by(Mmt.station).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tob():
    mindate = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    sel2 = [func.min(Mmt.tobs),func.max(Mmt.tobs),func.avg(Mmt.tobs)]
    tob = session.query(*sel2).filter(Mmt.date > mindate).all()
    toblst = []
    for each in tob:
        tob_dict = {}
        tob_dict["TMin"] = each[0]
        tob_dict["TMax"] = each[1]
        tob_dict["TAvg"] = each[2]        
        toblst.append(tob_dict)
    return jsonify(toblst)


@app.route("/api/v1.0/<dates>")
def bydate(dates):
    breakdate = []
    breakdate =dates.split("$$")    
    mindate = breakdate[0]
    if len(breakdate) > 1:
        maxdate = breakdate[1]
    else:
        maxdate = '2018-10-20'
    
    sel3 = [func.min(Mmt.tobs),func.max(Mmt.tobs),func.avg(Mmt.tobs)]
    tob2 = session.query(*sel3).\
                        filter(Mmt.date >= mindate).\
                        filter(Mmt.date <= maxdate).\
                        all()
    toblst2 = []
    for each in tob2:
        tob_dict2 = {}
        tob_dict2["TMin"] = each[0]
        tob_dict2["TMax"] = each[1]
        tob_dict2["TAvg"] = each[2]        
        toblst2.append(tob_dict2)
    return jsonify(toblst2)




if __name__ == '__main__':
    app.run(debug=True)