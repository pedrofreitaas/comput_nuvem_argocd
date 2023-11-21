from flask import Flask, request, jsonify
import pickle
from time import sleep
from sys import path
from os import listdir, stat
from multiprocessing import Process
from subprocess import run
path.append("data/")
from ModelSchema import Model

app = Flask(__name__)

path_to_model_pickled = "data/model.pkl"
app.loaded_model = False

def load_pickled_model() -> bool:
    try:
        # if it throws, app.model isn't affected.
        model_temp = pickle.load(open(path_to_model_pickled, "rb"))

        app.model = model_temp
        app.loaded_model = True
        run(f"echo Found pickled model, finishing search.", shell=True)
        return True
    
    except FileNotFoundError as e:
        run("echo Pickled model was not loaded because it is file does not exist.", shell=True)
        return False

# loading for the first time.
while not load_pickled_model(): 
    run(f"echo Did not find pickled model, waiting 15s to search again.", shell=True)
    sleep(15)

# checking periodically for updates, and 
def checks_for_new_pickle() -> None:
    timestamp = stat(path_to_model_pickled).st_mtime

    while True:
        try:
            new_tmp = stat(path_to_model_pickled).st_mtime
            if timestamp != new_tmp:
                timestamp = new_tmp
                try: 
                    load_pickled_model()
                    run(f"echo Found a new pickled model, updated API to it.", shell=True)
                except Exception as e:
                    run(f"echo Found update for model, but could not update. Reason: {e}.", shell=True)
        
        except FileNotFoundError:
            run("echo ALERT: Pickled model disappeard. Using the previous loaded version.", shell=True)
        
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