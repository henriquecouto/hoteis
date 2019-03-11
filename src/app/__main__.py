import os

from bottle import Bottle

from reservas import reservasApp
from clientes import clientesApp
from quartos import quartosApp

root = Bottle()

root.mount('/reservas', reservasApp)
root.mount('/clientes', clientesApp)
root.mount('/quartos', quartosApp)

if os.environ.get('APP_LOCATION') == 'heroku':
    root.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    root.run(host='localhost', port=8080, debug=True, reloader=True)
