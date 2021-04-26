#!/usr/bin/env python3

# Generates Goby3 protobuf configuration using definitions and text substitution
# Usage: python3 example.pb.cfg.py app_name

import sys
import os
from goby import config
import common, common.origin, common.topside, common.comms, common.sim

log_file_dir = common.jaia_log_dir+ '/topside'
os.makedirs(log_file_dir, exist_ok=True)

vehicle_id = 0 
wifi_modem_id = common.comms.wifi_modem_id(vehicle_id)
vehicle_type= 'TOPSIDE'

templates_dir=common.jaia_templates_dir

app_common = config.template_substitute(templates_dir+'/_app.pb.cfg.in',
                                        app=common.app,
                                        tty_verbosity = 'QUIET',
                                        log_file_dir = log_file_dir,
                                        log_file_verbosity = 'QUIET',
                                        warp=common.sim.warp,
                                        lat_origin=common.origin.lat(),
                                        lon_origin=common.origin.lon())

interprocess_common = config.template_substitute(templates_dir+'/_interprocess.pb.cfg.in',
                                                 platform='topside')


link_wifi_block = config.template_substitute(templates_dir+'/_link_wifi.pb.cfg.in',
                                                  subnet_mask=common.comms.subnet_mask,
                                                  modem_id=wifi_modem_id,
                                                  mac_slots=common.comms.wifi_mac_slots(vehicle_id))


if common.app == 'gobyd':    
    print(config.template_substitute(templates_dir+'/gobyd.pb.cfg.in',
                                     app_block=app_common,
                                     interprocess_block = interprocess_common,
                                     link_block=link_wifi_block))
elif common.app == 'goby_opencpn_interface':
    print(config.template_substitute(templates_dir+'/topside/goby_opencpn_interface.pb.cfg.in',
                                     app_block=app_common,
                                     interprocess_block = interprocess_common))
else:
    sys.exit('App: {} not defined'.format(common.app))
