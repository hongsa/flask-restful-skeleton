import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/{app_name}/')

activate_this = '/var/www/{app_name}/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from apps import app as application
application.secret_key = '{password}'