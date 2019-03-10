from bottle import Bottle

from subapps.reservas import reservasApp
from subapps.clientes import clientesApp

app = Bottle()

app.mount('/reservas', reservasApp)
app.mount('/clientes', clientesApp)

if __name__ == '__main__':
    app.run(debug=True, reloader=True, port=8080, host='localhost')
