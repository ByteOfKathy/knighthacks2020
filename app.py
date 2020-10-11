from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
import fleetController
from fleetController import Drone, FleetController
from fleetController import Vector3

app = Flask(__name__)
fc = fleetController.FleetController()
client = MongoClient()

db = client['knighthacks']
col = db['drones']

@app.route('/clear', methods = ['POST'])
def dropCollection():
    col.drop()
    fc.nextDroneId = 0
    fc.all_drones = []
    print("Collection cleared")
    return "Collection cleared"


@app.route('/', methods = ['GET'])
def testWorking():
    return json.dumps({'status' : 'It\'s working :D'})

@app.route('/addDrone', methods = ['POST'])
def savePositions():
    data = request.get_json()
    drone: Drone = fc.addNewDrone(data['x'], data['y'], data['z'])
    data["id"] = drone.id
    col.insert_one(data)
    #return json.dumps([doc for doc in col.find({"id" : data["id"]}, { "addresses": { "$slice": [0, 1] }, "_id": 0})])
    return str(drone.id)

@app.route('/updateDronePosition', methods = ['POST'])
def updatePos():
    data = request.get_json()
    col.update_one({'id': data['id']}, 
    {'$set' : {
        'x' : data['x'],
        'y' : data['y'],
        'z' : data['z']}
    })
    return json.dumps({'status' : 'finished'})

@app.route('/getDrone', methods = ['GET'])
def getDrone():
    data = request.get_json()
    ret = {}
    for item in col.find(data, {"_id" : 0}):
        ret['id'] = str(item['id'])
        ret['x'] = str(item['x'])
        ret['y'] = str(item['y'])
        ret['z'] = str(item['z'])
    return ret

@app.route('/moveFleetToPoint', methods = ['POST'])
def moveFleetToPoint():
    data = request.get_json()
    res = {}
    myVect = Vector3(float(data['x']), float(data['y']), float(data['z']))
    targets = fc.getDroneLocationsAboutPoint(myVect)
    fc.assignFirstMatchTaken(targets)
    drone: Drone
    res["drones"] = []
    for drone in fc.all_drones:
        if drone.target != None:
            info = {'id': drone.id, 'x': drone.target.position.x, 'y': drone.target.position.y, 'z': drone.target.position.z}
            res["drones"].append(info)
    return json.dumps(res)

@app.route('/getAllDrones', methods = ['GET'])
def getAllDrones():
    data = list(col.find({}, { "addresses": { "$slice": [0, 1] }, "_id": 0}))
    return json.dumps(data)

def registerExistingDrones():
    all_drones = json.loads(getAllDrones())
    for drone in all_drones:
        fc.registerExistingDrone(drone['id'], drone['x'], drone['y'], drone['z'])

registerExistingDrones()

if __name__ == "__main__":
    app.run()
