import os
import sys
import goby
from enum import Enum

def check_args():
    if len(sys.argv) >= 2:
        app=sys.argv[1]
    else:
        goby.config.fail('App name must be given as first command line argument')

check_args()
app=sys.argv[1]

try:
    jaia_n_auvs=int(os.environ['jaia_n_auvs'])
except:    
    goby.config.fail('Must set jaia_n_auvs environmental variable.')

try:
    jaia_log_dir=os.environ['jaia_log_dir']
    os.makedirs(jaia_log_dir, exist_ok=True)
except:    
    goby.config.fail('Must set jaia_log_dir environmental variable.')


jaia_templates_dir=os.path.normpath(os.path.dirname(os.path.realpath(__file__)) +  '/../../templates')
goby.config.checkdir(jaia_templates_dir)



class Mode(Enum):
     RUNTIME = "runtime"
     SIMULATION = "simulation"     

try:
    jaia_mode=Mode(os.environ['jaia_mode'])
except:    
    goby.config.fail('Must set jaia_mode environmental variable to "runtime" or "simulation".')


def is_simulation():
    return jaia_mode == Mode.SIMULATION
def is_runtime():
    return jaia_mode == Mode.RUNTIME


def app_block(verbosities, debug_log_file_dir, geodesy):
    default_verbosities = {'runtime': {'tty': 'WARN', 'log': 'WARN'}, 'simulation': {'tty': 'QUIET', 'log': 'QUIET'}}
    app_verbosity = verbosities.get(app, default_verbosities)

    if is_simulation():
        simulation_block = goby.config.template_substitute(jaia_templates_dir+'/_simulation.pb.cfg.in',
                                                      warp=sim.warp)
        tty_verbosity = app_verbosity['simulation']['tty']
        log_verbosity = app_verbosity['simulation']['log']
    elif is_runtime():
        simulation_block = ""
        tty_verbosity = app_verbosity['runtime']['tty']
        log_verbosity = app_verbosity['runtime']['log']
    
    return goby.config.template_substitute(jaia_templates_dir+'/_app.pb.cfg.in',
                                           app=app,
                                           tty_verbosity = tty_verbosity,
                                           log_file_dir = debug_log_file_dir,
                                           log_file_verbosity = log_verbosity,
                                           simulation=simulation_block,
                                           geodesy=geodesy)
