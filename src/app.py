from bottle import Bottle

from subapps.reservas import reservasApp

app = Bottle()

app.mount('/reservas', reservasApp)

if __name__ == '__main__':
    app.run(debug=True, reloader=True, port=8080, host='localhost')
