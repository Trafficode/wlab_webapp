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

@application.route("/restq/stations/desc")
def stations_desc():
    logger.info("stationsdesc()")   
    return ipc_send_receive(Config.IPC_DP_SERVER_PORT, 
                            'GET_DESC', 
                            json.dumps({}), 
                            1)

@application.route("/restq/stations/newest")
def stations_newest():
    logger.info("stationsdesc()")
    return ipc_send_receive(Config.IPC_DP_SERVER_PORT, 
                            'GET_NEWEST', 
                            json.dumps({}), 
                            1)

@application.route("/restq/stations/datatree")
def stations_datatree():
    logger.info("stations_datatree()")
    return ipc_send_receive(Config.IPC_DP_SERVER_PORT, 
                            'GET_DATATREE', 
                            json.dumps({}), 
                            1)

@application.route("/restq/station/serie/daily/<string:uid_serie_date>")
def station_dailyserie(uid_serie_date):
    logger.info("station_dailyserie()")
    param = json.loads(uid_serie_date)
    logger.info("param; %s" % str(param))
    return ipc_send_receive(Config.IPC_DP_SERVER_PORT, 
                            'GET_DAILY', 
                            uid_serie_date, 
                            1)

@application.route("/restq/station/serie/monthly/<string:uid_serie_date>")
def station_monthlyserie(uid_serie_date):
    logger.info("station_monthlyserie()")
    param = json.loads(uid_serie_date)
    logger.info("param; %s" % str(param))
    return ipc_send_receive(Config.IPC_DP_SERVER_PORT, 
                            'GET_MONTHLY', 
                            uid_serie_date, 
                            1)

@application.route("/restq/station/serie/yearly/<string:uid_serie_date>")
def station_yearlyserie(uid_serie_date):
    logger.info("station_yearlyserie()")   
    param = json.loads(uid_serie_date)
    logger.info("param; %s" % str(param))
    return ipc_send_receive(Config.IPC_DP_SERVER_PORT, 
                            'GET_YEARLY', 
                            uid_serie_date, 
                            1)

if __name__ == '__main__':
    logger.critical("run from directory %s" % str(os.getcwd()))
    logger.critical("VERSION: " + Config.WLAB_VERSION)
    application.run(host='0.0.0.0', debug=True, use_reloader=False)

#   ------------------------------------------------------------------------- /
#    end of file
#   ------------------------------------------------------------------------- /
