from main import MeasureThread
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

measure = MeasureThread()

# This runs on an older version of Python, so we can't use Flask >2.0.0
@app.route('/all', methods=["GET"])
def get_all():
    return jsonify(measure.list_adc)

@app.route('/cap', methods=["POST", "GET"])
def cap():
    if request.method == "GET":
        return jsonify({"time":measure.client.get("capacitor_sleep").decode()})

    if "time" not in request.json:
        return "Bad Request", 400

    try:
        measure.client.set("capacitor_sleep", request.json.get("time"))
    except ValueError:
        return "Invalid Period Supplied", 400

    return "OK", 200

@app.route('/zero', methods=["DELETE"])
def zero():
    #global list_adc
    with measure.list_lock:
        measure.list_adc = [0]*4096
    return "OK", 200

def create_app():
    measure.start()
    return app

