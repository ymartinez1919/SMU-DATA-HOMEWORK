import numpy as np
import pandas as pd
from flask import Flask, jsonify
from sqlalchemy import create_engine



#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#set up my Database
path = "sqlite:///Resources/hawaii.sqlite"
engine = create_engine(path)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of prcp totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of all stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of temperature observations (TOBS) of the most active station for the last year of data<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"- When given only the start date (YYYY-MM-DD), calculate the temperature MIN/AVG/MAX for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"- When given the start and end date (YYYY-MM-DD), calculate the temperature MIN/AVG/MAX for dates between the start and end date<br/>"
         )


#################################################
@app.route("/api/v1.0/precipitation")
def pcrp():
    conn = engine.connect()
    query = """
        SELECT
            station,
            date,
            prcp
        FROM
            measurement
       ORDER BY
           station asc,
           date asc;
        """
    df = pd.read_sql(query, conn)

    conn.close()

    data = df.to_dict(orient="records")
    return(jsonify(data))


#########################################
@app.route("/api/v1.0/stations")
def stationnames():
    conn = engine.connect()

    query = """
        SELECT
            station,
            name
        FROM
            station;
        """
    df = pd.read_sql(query, conn)

    conn.close()

    data = df.to_dict(orient="records")
    return(jsonify(data))


####################################
@app.route("/api/v1.0/tobs")
def temps():
    conn = engine.connect()
    query = """
        SELECT
          station,
          date,
          tobs
          
        FROM
            measurement
        WHERE
            date >= '2016-08-23'
        AND
            station = 'USC00519281'
        ORDER BY
            date asc;
        """
    df = pd.read_sql(query, conn)

    conn.close()

    data = df.to_dict(orient="records")
    return(jsonify(data))


######################################
@app.route("/api/v1.0/<start>")
def startrange (start):
    conn = engine.connect()
    query = f"""
        SELECT
            min(tobs) as TMIN,
            avg(tobs) as TAVG,
            max(tobs) as TMAX
        FROM
            measurement
        WHERE
            date >= '{start}'
        """
    df = pd.read_sql(query, conn)

    conn.close()

    data = df.to_dict(orient="records")
    return(jsonify(data))


#####################################
@app.route("/api/v1.0/<start>/<end>")
def startendrange (start,end):
    conn = engine.connect()
    query = f"""
        SELECT
            min(tobs) as TMIN,
            avg(tobs) as TAVG,
            max(tobs) as TMAX
        FROM
            measurement
        WHERE
            date >= '{start}'
        AND 
            date <= '{end}'
        """
    df = pd.read_sql(query, conn)

    conn.close()

    data = df.to_dict(orient="records")
    return(jsonify(data))


if __name__ == '__main__':
    app.run(debug=True)
