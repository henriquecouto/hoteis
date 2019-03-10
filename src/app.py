from bottle import Bottle, request, response
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps
import json

app = Bottle()
database_name = 'heroku_4q7l2460'
db_uri = 'mongodb://hoteis:oioi12@ds137336.mlab.com:37336/heroku_4q7l2460'
db_plugin = MongoPlugin(uri=db_uri, db=database_name, json_mongo=True)

app.install(db_plugin)


@app.route('/reservas', method='POST')
def createReserva(mongodb):
    newReserva = request.json

    query = mongodb['reservas'].find({'quarto': newReserva['quarto']})

    reservas = dumps(query)

    disponivel= True
    status= 'Reserva Disponível'

    if(newReserva['saida'] < newReserva['entrada']):
        return {'result': 'A data de entrada deve ser antes da data de saída'}
    else:
        for reserva in json.loads(reservas):
            if (reserva['saida'] >= newReserva['entrada']) and (reserva['entrada'] <= newReserva['saida']) :
                disponivel = False
                status = 'Reserva não disponível'

    if(disponivel):
        # criar reserva
        return {'result': status}
    else:
        return {'result': status}

if __name__ == '__main__':
    app.run(debug=True, reloader=True, port=8080, host='localhost')
