#SQL-Alchemy HW

#51:09

# 1. Import Flask
from flask import Flask

#2. creat app
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
    )

date = {}
prcp = {}
@app.route("/api/v1.0/precipitation")
def Precipitation():
    return jsonify(f"x")


stations = {}
@app.route("/api/v1.0/stations")
def Stations():
    return jsonify(f"x")



@app.route("/api/v1.0/tobs")
def Tobs():
    return jsonify(f"x")

if __name__ == "__main__":
    app.run(debug=True)    