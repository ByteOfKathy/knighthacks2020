from flask import Flask, request, jsonify
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
    col.update_one({'id': data['id']}, 
    {'$set' : {
        'x' : data['x'],
        'y' : data['y'],
        'z' : data['z']}
    })
    return json.dumps({'status' : 'finished'})

@app.route('/test/getDronePositions', methods =  ['GET'])
def getPositions():
    ret = {}
    cnt = 0
    for i in col.find():
        ret[str(cnt)] = jsonify(str(i))
        cnt += 1
    return ret


if __name__ == "__main__":
    app.run()