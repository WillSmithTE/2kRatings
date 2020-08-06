import pickle

def save(data, filename):
    file = open(filename, 'ab')
    pickle.dump(data, file)
    file.close()

def read(filename):
    try:
        file = open(filename, 'rb')      
        data = pickle.load(file) 
        file.close()
        return data
    except:
        return None