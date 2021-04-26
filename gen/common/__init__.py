import os
import sys
import goby

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

