# Import the dependencies.con
from flask import Flask, url_for, jsonify
import datetime as dt
import numpy as np
import sqlalchemy
#####import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func############################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base=automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine,reflect=True)


# Assign the measurement class to a variable called `Measurement` and
Measurement=Base.classes['measurement']
Station=Base.classes['station']

# the station class to a variable called `Station`


# Create a session
session=Session(engine)

#################################################
# Flask Setup
#################################################

app=Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    links = ['/api/v1.0/precipitation','/api/v1.0/stations','/api/v1.0/tobs','/api/v1.0/<start>','/api/v1.0/<start>/<end>']
    return links
@app.route('/api/v1.0/precipitation')
def precipitation():
    session=Session(engine)
    r=session.query(Measurement).filter(Measurement.date>'01-01-2017').with_entities(Measurement.date,Measurement.prcp).all()
    records=list(np.ravel(r))
    session.close()
    return jsonify(records)
@app.route('/api/v1.0/stations')
def stations():
    session=Session(engine)
    stations=[]
    for station in session.query(Station).with_entities(Station.station):
        stations.append(station)
    session.close()
    return jsonify(list(np.ravel(stations)))
@app.route('/api/v1.0/tobs')
def temps():
    session=Session(engine)
    results=session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    station=results[0][0]
    last_year=dt.date(2017,8,23)-dt.timedelta(days=365)
    data=session.query(Measurement.date,Measurement.tobs).filter(Measurement.station==station).filter(Measurement.date>last_year).all()
    records=list(np.ravel(data))
    session.close()
    return jsonify(records)
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def stats(start,*end):
    session=Session(engine)
    sel=[func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    if end:
        data=session.query(*sel).filter(Measurement.date<=end).filter(Measurement.date>start).all()
    else:
        data=session.query(*sel).filter(Measurement.date>start).all()
    records=list(np.ravel(data))
    session.close()
    return jsonify(records)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100)