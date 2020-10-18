#!/usr/bin/python

#-*- coding: utf-8 -*-
#   ------------------------------------------------------------------------- /
#   wlab_webapp: wlabapp.py
#   Created on: 29 sie 2019
#   Author: Trafficode
#   ------------------------------------------------------------------------- /

import os
import json
import logging
from globals import Globals
from ipc import ipc_send_receive

if os.path.exists(Globals.RELEASE_CONFIG_FILE):
    config_f = open(Globals.RELEASE_CONFIG_FILE, 'r')
    Config = json.load(config_f)
    config_f.close()
else:
    # develop mode
    Config = {
        "logging_path": "../../log/",
        "socket_file_path": "../sock"
    }
    
if not os.path.exists(Config['logging_path']):
    os.mkdir(Config['logging_path'])

logging.basicConfig(
    filename = os.path.join(Config['logging_path'], 'wlabapp.log'), 
    format = '%(asctime)s - %(name)-24.24s - %(levelname)8s - %(message)s', 
    atefmt = '%m/%d/%Y %I:%M:%S %p'
)

from flask import Flask
from flask import render_template

logger = logging.getLogger('wlabapp')
logger.setLevel(logging.INFO)

application = Flask(__name__)
@application.route('/')
@application.route('/index')
def index():
    logger.info("index()")
    return render_template("index.html", title="Home")
 
@application.route('/globals/version')
def wlabversion():
    logger.info("wlabversion()")
    version_data = {"version": Globals.WLAB_VERSION,
                       "date": Globals.WLAB_COMMIT_DATE}
    return json.dumps(version_data)
  
@application.route("/restq/stations/desc")
def stations_desc():
    logger.info("stationsdesc()")   
    return ipc_send_receive(Config['socket_file_path'], 
                            'GET_DESC', 
                            json.dumps({}), 
                            1)
  
@application.route("/restq/stations/newest")
def stations_newest():
    logger.info("stationsdesc()")
    return ipc_send_receive(Config['socket_file_path'], 
                            'GET_NEWEST', 
                            json.dumps({}), 
                            1)
  
@application.route("/restq/stations/datatree")
def stations_datatree():
    logger.info("stations_datatree()")
    return ipc_send_receive(Config['socket_file_path'], 
                            'GET_DATATREE', 
                            json.dumps({}), 
                            1)
  
@application.route("/restq/station/serie/daily/<string:uid_serie_date>")
def station_dailyserie(uid_serie_date):
    logger.info("station_dailyserie()")
    param = json.loads(uid_serie_date)
    logger.info("param <%s>" % str(param))
    return ipc_send_receive(Config['socket_file_path'], 
                            'GET_DAILY', 
                            uid_serie_date, 
                            1)
  
@application.route("/restq/station/serie/monthly/<string:uid_serie_date>")
def station_monthlyserie(uid_serie_date):
    logger.info("station_monthlyserie()")
    param = json.loads(uid_serie_date)
    logger.info("param <%s>" % str(param))
    return ipc_send_receive(Config['socket_file_path'], 
                            'GET_MONTHLY', 
                            uid_serie_date, 
                            1)
  
@application.route("/restq/station/serie/yearly/<string:uid_serie_date>")
def station_yearlyserie(uid_serie_date):
    logger.info("station_yearlyserie()")   
    param = json.loads(uid_serie_date)
    logger.info("param <%s>" % str(param))
    return ipc_send_receive(Config['socket_file_path'], 
                            'GET_YEARLY', 
                            uid_serie_date, 
                            4)
  
if __name__ == '__main__':
    logger.critical("run from directory %s" % str(os.getcwd()))
    logger.critical("VERSION: " + Globals.WLAB_VERSION)
    application.run(host='0.0.0.0', debug=True, use_reloader=False)

#   ------------------------------------------------------------------------- /
#    end of file
#   ------------------------------------------------------------------------- /
