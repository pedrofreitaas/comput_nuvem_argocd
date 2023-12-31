from os.path import exists
import sys, pickle
from os import listdir, remove
from os.path import splitext
from subprocess import run
sys.path.append("project2-pv/")
from ModelSchema import Model

def create(path: str) -> Model:
    if not exists(path) or asked_for_reinit(): 
        run('echo Created new model.', shell=True)
        return Model()

    run('echo Using existing model.', shell=True)
    return pickle.load(open(path, 'rb'))

def save(path) -> None:
    try: remove(path)
    except FileNotFoundError: pass

    with open(path, 'wb') as f:
        pickle.dump(m1, f)

def get_file_extension(file_path):
    _, extension = splitext(file_path)
    return extension.lower()

def get_file_to_train() -> str:
    try:
        return "data/" + sys.argv[sys.argv.index("-t")+1]
    except ValueError:
        return "data/"

def asked_for_reinit() -> bool:
    try: 
        i = sys.argv.index("-r")
        return True
    except ValueError:
        return False

if __name__ == "__main__":    
    path_to_pickle = "project2-pv/model.pkl"
    
    m1 = create(path_to_pickle)
    
    try:
        filepath = get_file_to_train()
        
        if get_file_extension(filepath) != ".csv": raise FileNotFoundError
        
        run(f'echo "Training with data: {filepath}."', shell=True)
        
        m1.train(filepath)
            
        save(path_to_pickle)

        run(f"echo Success. Saved new model.", shell=True)
        
    except Exception as e:
        run(f'echo "Training failed for {filepath}. Reason: {e}"', shell=True)

    print(m1)
