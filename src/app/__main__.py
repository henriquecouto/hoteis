import os

from bottle import Bottle

from reservas import reservasApp
from clientes import clientesApp
from quartos import quartosApp

root = Bottle()

root.mount('/reservas', reservasApp)
root.mount('/clientes', clientesApp)
root.mount('/quartos', quartosApp)

# heroku
root.run(server='gevent', port=os.environ.get('PORT', 5000))

# Local
# root.run(host='localhost', port=8081, debug=True, reloader=True)
