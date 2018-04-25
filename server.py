from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
import socket

db_connect = create_engine('sqlite:///JMU_Autonomous.db')
app = Flask(__name__)
api = Api(app)

class Locations(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from Locations") # This line performs query and returns json result
        result = {'Locations': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class addLocation(Resource):
    def get(self, location_info):
        info = location_info.split("+")
        str = "INSERT INTO Locations VALUES (" + info[0] + ", \'" + info[1].replace("_", " ") + "\', \'" + info[2].replace("_", " ") + "\', " + info[3] + ", " + info[4] + ");"

        conn = db_connect.connect() # connect to database
        query = conn.execute(str) # This line performs query and returns json result
        return "success"

class deleteLocation(Resource):
    def get(self, location_name):
        info = location_name.replace("_", " ")
        str = "DELETE FROM Locations WHERE name=\'" + info + "\';"
        conn = db_connect.connect() # connect to database
        query = conn.execute(str) # This line performs query and returns json result
        return "success"

class Location_name(Resource):
    def get(self, location_name):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from Locations WHERE Name = '" + location_name + "'") # This line performs query and returns json result
        result =  {'Locations': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Cardata(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from Cardata") # This line performs query and returns json result
        result = {'Cardata': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)   

    def post(self):
        conn = db_connect.connect() # connect to database

        req = request.get_json()
        newData = req['newData']

        battery = newData['battery']
        camera = newData['camera']
        elevation = newData['elevation']
        lat = newData['lat']
        lightware = newData['lightware']
        lon = newData['lon']
        rplidar = newData['rplidar']
        timestamp = newData['timestamp']
        velocity = newData['velocity']
        velodyne = newData['velodyne']

        #clear the table
        conn.execute("DELETE FROM Cardata;");

        query = "INSERT INTO Cardata VALUES (" + str(velocity) + ", " + str(lat) + ", " + str(lon) + ", " + str(elevation) + ", \"" + str(battery) + "\", \"" + str(velodyne) + "\", \"" + str(lightware) + "\", \"" + str(rplidar) + "\",  \"" + str(timestamp) + "\", \"" + str(camera) + "\");"


        conn.execute(query);
            #print "INSERT INTO Goals VALUES (" + str(lat) + "," + str(lon) + "," + str(elevation) +");"

        return "Car data updated"

class battery_voltage(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute(" select battery from Cardata") # This line performs query and returns json result
        result =  {'battery_voltage': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} 
        return jsonify(result)

class camera_status(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute(" select camera from Cardata") # This line performs query and returns json result
        result =  {'camera_status': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} 
        return jsonify(result)

class gps_status(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute(" select gps from Cardata") # This line performs query and returns json result
        result =  {'gps_status': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} 
        return jsonify(result)

class llidar_status(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute(" select lightware from Cardata") # This line performs query and returns json result
        result =  {'llidar_status': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} 
        return jsonify(result)

class rlidar_status(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute(" select rplidar from Cardata") # This line performs query and returns json result
        result =  {'rlidar_status': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} 
        return jsonify(result)

class velocity(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute(" select velocity from Cardata") # This line performs query and returns json result
        result =  {'velocity': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} 
        return jsonify(result)

class velodyne_status(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute(" select velodyne from Cardata") # This line performs query and returns json result
        result =  {'velodyne_status': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} 
        return jsonify(result)

class Goals(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from Goals") # This line performs query and returns json result
        result = {'Goals': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    def post(self):
        conn = db_connect.connect() # connect to database
        j = request.get_json()
        list_of_goals = j['goals']

        for item in list_of_goals:
            lat = item['lat']
            lon = item['long']
            elevation = item['elevation']
            conn.execute("INSERT INTO Goals VALUES (" + str(lat) + "," + str(lon) + "," + str(elevation) +");");
            #print "INSERT INTO Goals VALUES (" + str(lat) + "," + str(lon) + "," + str(elevation) +");"

        return 'goals added'

class clear_goals(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("delete from Goals") # This line performs query and returns json result
        #result = {'Goals': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return 'goals cleared'

api.add_resource(Locations, '/locations')
api.add_resource(Location_name, '/locations/<location_name>')
api.add_resource(addLocation, '/addlocation/<string:location_info>')
api.add_resource(deleteLocation, '/deletelocation/<string:location_name>')

api.add_resource(Cardata, '/cardata')
api.add_resource(battery_voltage, '/cardata/battery')
api.add_resource(camera_status, '/cardata/camera')
api.add_resource(gps_status, '/cardata/gps')
api.add_resource(llidar_status, '/cardata/llidar')
api.add_resource(rlidar_status, '/cardata/rlidar')
api.add_resource(velocity, '/cardata/velocity')
api.add_resource(velodyne_status, '/cardata/velodyne')

api.add_resource(Goals, '/goals')
api.add_resource(clear_goals, '/clear')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers',
                       'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods',
                       'GET,PUT,POST,DELETE,OPTIONS')
  return response




if __name__ == '__main__':
    #hostname = socket.gethostname()
    #dns_resolved_addr = socket.gethostbyname(hostname)
    #print(str(dns_resolved_addr))
    #app.run(host=str(dns_resolved_addr), port=8080)
    app.run(host='192.168.99.72', port=5000)
