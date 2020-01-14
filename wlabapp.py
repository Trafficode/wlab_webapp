#   ------------------------------------------------------------------------- /
#   wlab_web_dataprovider: dataprovider.py
#   Created on: 29 sie 2019
#   Author: Trafficode
#   ------------------------------------------------------------------------- /

import os
import json
import logging
from user_config import Config
from flask import Flask
from flask import render_template
from ipc import ipc_send_receive

if Config.DEVELOP:
    log_file_path = 'log/wlabapp.log'
    if not os.path.exists('log'):
        os.mkdir('log')
else:
    log_file_path = '/home/wlab/weatherlab/log/wlabapp.log'

logging.basicConfig(
    filename = log_file_path, 
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    atefmt = '%m/%d/%Y %I:%M:%S %p'
)
logger = logging.getLogger("wlabapp")

application = Flask(__name__)
@application.route('/')
@application.route('/index')
def index():
    logger.info("index()")
    return render_template("index.html", title="Home")

@application.route('/globals/version')
def wlabversion():
    logger.info("wlabversion()")
    version_data = {"version": Config.WLAB_VERSION,
                       "date": Config.WLAB_COMMIT_DATE}
    return json.dumps(version_data)



# --------------------------------------------------------------------------- /
# {
#     "A02938401234":
#     {
#         "description": "", 
#         "longitude": 42.28, 
#         "serie": {
#             "Temperature": 1, 
#             "Humidity": 2
#         }, 
#         "latitude": 25.22, 
#         "timezone": "Europe/Warsaw", 
#         "name": "Andromeda"
#     },
#     "142209325783":
#     {
#         "description": "", 
#         "longitude": 42.89, 
#         "serie": {
#             "Temperature": 1, 
#         }, 
#         "latitude": 20.22, 
#         "timezone": "Europe/Warsaw", 
#         "name": "Trello"
#     }
# }
@application.route("/restq/stations/desc")
def stations_desc():
    logger.info("stationsdesc()")
    stationsDesc = dataProvider.getStationsDesc()
    return json.dumps(stationsDesc)

if __name__ == '__main__':
    logger.critical("run from directory %s" % str(os.getcwd()))
    logger.critical("VERSION: " + Config.WLAB_VERSION)
    application.run(host='0.0.0.0', debug=True, use_reloader=False)
        
#   ------------------------------------------------------------------------- /
#    end of file
#   ------------------------------------------------------------------------- /
