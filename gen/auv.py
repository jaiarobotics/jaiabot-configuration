#!/usr/bin/env python3

# Generates Goby3 protobuf configuration using definitions and text substitution
# Usage: python3 example.pb.cfg.py app_name

import sys
import os
from goby import config
import common, common.origin, common.vehicle, common.comms, common.sim

try:
    number_of_auvs=int(os.environ['jaia_n_auvs'])
except:
    config.fail('Must set jaia_n_auvs environmental variable, e.g. "jaia_n_auvs=10 jaia_auv_index=0 ./auv.launch"')

try:
    auv_index=int(os.environ['jaia_auv_index'])
except:
    config.fail('Must set jaia_auv_index environmental variable, e.g. "jaia_n_auvs=10 jaia_auv_index=0 ./auv.launch"')

log_file_dir = common.jaia_log_dir+ '/auv/' + str(auv_index)
os.makedirs(log_file_dir, exist_ok=True)
templates_dir=common.jaia_templates_dir

vehicle_id=auv_index+common.comms.topside_vehicle_id+1
wifi_modem_id = common.comms.wifi_modem_id(vehicle_id)

app_common = config.template_substitute(templates_dir+'/_app.pb.cfg.in',
                                 app=common.app,
                                 tty_verbosity = 'QUIET',
                                 log_file_dir = log_file_dir,
                                 log_file_verbosity = 'QUIET',
                                 warp=common.sim.warp,
                                 lat_origin=common.origin.lat(),
                                 lon_origin=common.origin.lon())

interprocess_common = config.template_substitute(templates_dir+'/_interprocess.pb.cfg.in',
                                                 platform='auv'+str(auv_index))

link_wifi_block = config.template_substitute(templates_dir+'/_link_wifi.pb.cfg.in',
                                               subnet_mask=common.comms.subnet_mask,
                                               modem_id=wifi_modem_id,
                                               mac_slots=common.comms.wifi_mac_slots(vehicle_id))
link_block=link_wifi_block

if common.app == 'gobyd':    
    print(config.template_substitute(templates_dir+'/gobyd.pb.cfg.in',
                                     app_block=app_common,
                                     interprocess_block = interprocess_common,
                                     link_block=link_block))
elif common.app == 'goby_logger':    
    print(config.template_substitute(templates_dir+'/goby_logger.pb.cfg.in',
                                     app_block=app_common,
                                     interprocess_block = interprocess_common,
                                     goby_logger_dir=log_file_dir))
elif common.app == 'goby_frontseat_interface_basic_simulator':
    print(config.template_substitute(templates_dir+'/auv/frontseat.pb.cfg.in',
                                     moos_port=common.vehicle.moos_port(vehicle_id),
                                     app_block=app_common,
                                     interprocess_block = interprocess_common,
                                     sim_start_lat = common.origin.lat(),
                                     sim_start_lon = common.origin.lon(),
                                     sim_port = common.vehicle.simulator_port(vehicle_id)))
elif common.app == 'moos':
    print(config.template_substitute(templates_dir+'/auv/auv.moos.in',
                                     moos_port=common.vehicle.moos_port(vehicle_id),
                                     moos_community='AUV' + str(auv_index),
                                     warp=common.sim.warp,
                                     lat_origin=common.origin.lat(),
                                     lon_origin=common.origin.lon(),
                                     bhv_file='/tmp/auv' + str(auv_index) + '.bhv'))
elif common.app == 'bhv':
    print(config.template_substitute(templates_dir+'/auv/auv.bhv.in'))
    
elif common.app == 'frontseat_sim':
    print(common.vehicle.simulator_port(vehicle_id))
else:
    sys.exit('App: {} not defined'.format(common.app))
