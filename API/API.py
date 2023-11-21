from flask import Flask, request, jsonify
import pickle
from time import sleep
from sys import path
from os import listdir, stat
from multiprocessing import Process
path.append("data/")
from ModelSchema import Model

app = Flask(__name__)

path_to_model_pickled = "data/model.pkl"
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

def checks_for_new_pickle() -> None:
    timestamp = stat(path_to_model_pickled).st_mtime

    while True:
        new_tmp = stat(path_to_model_pickled).st_mtime
        if timestamp != new_tmp:
            timestamp = new_tmp
            try: 
                load_pickled_model()
                print('Updated model.')
            except Exception as e:
                print(f"Found update for model, but couldn't update. Reason: {e}.")
        sleep(15)

p = Process(target=checks_for_new_pickle)
p.start()

@app.route("/api/recommend", methods=["POST"])
def recommend():
    if not app.loaded_model: 
        return {"ERROR": "Server wasn't able to recommend"}.json()

    playlists_ids = request.get_json(force=True)["songs"]
    return jsonify(app.model.recommend(playlists_ids))

app.run(host="0.0.0.0", port=5000)
p.kill()