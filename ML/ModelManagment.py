from os.path import exists
import sys, pickle
from os import listdir
from os.path import splitext
sys.path.append("/app/project2-pv/")
from ModelSchema import Model

def create(path: str) -> Model:
    if not exists(path): return Model()
    return pickle.load(open(path, 'rb'))

def save(path) -> None: 
    with open(path, 'wb') as f:
        pickle.dump(m1, f)

def get_file_extension(file_path):
    _, extension = splitext(file_path)
    return extension.lower()

def get_file_to_train() -> str:
    return "data/" + sys.argv[sys.argv.indexOf("-t")+1]

if __name__ == "__main__":    
    path_to_pickle = "project2-pv/model.pkl"
    
    m1 = create(path_to_pickle)
    
    try:
        filepath = get_file_to_train()
        
        if get_file_extension(filepath) != ".csv": continue
        
        print('Training with data: ' + filepath)
        
        try: m1.train(filepath)
        except Exception:
            print("Training didn't succeed for: " + filepath)
            
        print('Success.')
        
    except Exception as e:
        print('Training failed. Reason: ', e)

    save(path_to_pickle)
    print(m1)
