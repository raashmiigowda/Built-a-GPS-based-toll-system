from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from geopy.distance import geodesic
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["toll_system"]
collection = db["transactions"]

TOLL_LOCATION = (12.9716, 77.5946)
RADIUS = 0.5
TOLL_AMOUNT = 50

user_balance = {"vehicle_1": 500}

def is_inside_toll(lat, lon):
    distance = geodesic((lat, lon), TOLL_LOCATION).km
    return distance <= RADIUS

@app.route('/location', methods=['POST'])
def receive_location():
    data = request.json
    vehicle_id = data['vehicle_id']
    lat = data['latitude']
    lon = data['longitude']

    inside = is_inside_toll(lat, lon)

    if inside:
        if user_balance[vehicle_id] >= TOLL_AMOUNT:
            user_balance[vehicle_id] -= TOLL_AMOUNT

            transaction = {
                "vehicle_id": vehicle_id,
                "amount": TOLL_AMOUNT,
                "location": [lat, lon],
                "timestamp": datetime.now()
            }
            collection.insert_one(transaction)

            return jsonify({"status": "Toll Deducted", "balance": user_balance[vehicle_id]})

    return jsonify({"status": "Outside Toll Zone"})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    data = list(collection.find().sort("_id", -1))
    for d in data:
        d["_id"] = str(d["_id"])
    return jsonify(data)

@app.route('/balance/<vehicle_id>', methods=['GET'])
def get_balance(vehicle_id):
    return jsonify({"balance": user_balance.get(vehicle_id, 0)})

if __name__ == '__main__':
    app.run(debug=True)
