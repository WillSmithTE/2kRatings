import logging
from model.Data import Data
from service.DataService import DataService
import os
from controller.Controller import Controller
from util.util import read
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig()
logging.root.setLevel(logging.INFO)

data = None

if os.environ.get('CACHE', True) == True:
    data = read('data.pickle')
    if data is None:
        data = Data()
        dataService = DataService(data)
        dataService.getAndCacheAllData()

else:
    data = Data()
    dataService = DataService(data)
    dataService.getAllData()


app = Flask(__name__)
CORS(app)
Controller(app, data)
