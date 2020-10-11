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
    col.insert_one(data)
    return json.dumps({
        'status' : 'finished',
        'Added' : col.count()
    })

@app.route('/updateDronePositions', methods = ['POST'])
def updatePos():
    data = request.get_json()
    col.update_one(data['query'], {'$set' : data['updateData']})
    return json.dumps({'status' : 'finished'})

@app.route('/test/getDronePositions', methods =  ['GET'])
def getPositions():
    return json.dumps(col.find())


if __name__ == "__main__":
    app.run()