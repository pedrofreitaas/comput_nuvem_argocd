from flask import Flask, request, jsonify
import pickle
from time import sleep
from sys import path
from os import stat
from multiprocessing import Process
from subprocess import run
path.append("data/")
from ModelSchema import Model

path_to_model_pickled = "data/model.pkl"

def API(model: object):
    app = Flask(__name__)

    @app.route("/api/recommend", methods=["POST"])
    def recommend():
        if model == None:
            return {"ERROR": "Server wasn't able to recommend."}.json()

        playlists_ids = request.get_json(force=True)["songs"]
        return jsonify(model.recommend(playlists_ids))
    
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    timestamp = None
    update_tick_seconds = 15
    p_API = Process(target=API, args=[None])

    while True:
        try: 
            new_tmp = stat(path_to_model_pickled).st_mtime

            if new_tmp != timestamp:
                # updating API.
                if p_API.is_alive(): p_API.kill()

                model = pickle.load(open(path_to_model_pickled,'rb'))
                p_API = Process(target=API, args=[model])
                p_API.start()
                
                if timestamp == None:  run('echo Found pickled MODEL. Started API!!!', shell=True)
                else: run('echo Found new MODEL version. Updated API.', shell=True)
                
                timestamp = new_tmp

                sleep(update_tick_seconds)
            
        except FileNotFoundError:
            # IDLE API already running.
            if p_API.is_alive(): continue

            # setting IDLE API.
            p_API.start()
            run('echo Pickled model was not found. Running IDLE API.', shell=True)

            sleep(update_tick_seconds)