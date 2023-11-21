from flask import Flask, request, jsonify
import pickle
from time import sleep
from sys import path
from os import listdir
path.append("/app/data/")
from ModelSchema import Model

app = Flask(__name__)

path_to_model_pickled = "/app/data/model.pkl"
app.loaded_model = False

def load_pickled_model() -> bool:
    try:
        app.model = pickle.load(open(path_to_model_pickled, "rb"))
        app.loaded_model = True
        return True
    except FileNotFoundError as e:
        print("Pickled model wasn't loaded because it's file doesn't exist.", e)
        return False

while not load_pickled_model(): sleep(15)

@app.route("/api/recommend", methods=["POST"])
def recommend():
    if not app.loaded_model: 
        return {"ERROR": "Server wasn't able to recommend"}.json()

    playlists_ids = request.get_json(force=True)["songs"]
    return jsonify(app.model.recommend(playlists_ids))

app.run(host="0.0.0.0", port=5000)