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
    for(i in range(data['size']))
        col.insert(data)
    return json.dumps({'status' : 'finished'})

@app.route('/test/getDronePositions', methods =  ['GET'])
def getPositions():
    return(json.dumps({'status' : 'WIP'}))


if __name__ == "__main__":
    app.run()