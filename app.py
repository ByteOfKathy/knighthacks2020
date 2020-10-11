from flask import Flask, request
from pymongo import MongoClient
import json

app = Flask(__name__)
client = MongoClient()

db = client['knighthacks']
col = db['drones']

@app.route('/', methods = ['GET'])
def testWorking():
    return json.dumps({'status' : 'It\'s working :D'})

@app.route('/dronePositions', methods = ['POST'])
def savePositions():
    data = request.get_json()
    if int(col.count()) is 0:
        for i in range(int(data['size'])):
            col.insert_one(data['drones'][str(i)], data['drones'])
    else:
        for i in range(int(data['size'])):
            col.update_one(data['drones'][str(i)], {'$set' : data['drones']})
    return json.dumps({'status' : 'finished'})

@app.route('/test/getDronePositions', methods =  ['GET'])
def getPositions():
    return json.dumps(col.find())


if __name__ == "__main__":
    app.run(debug = True)