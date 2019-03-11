from bottle import Bottle, request, response
from bson.json_util import dumps
import json
from database import db_plugin

quartosApp = Bottle()
quartosApp.install(db_plugin)


# Listar Quartos
@quartosApp.get('/')
def getAllQuartos(mongodb):
    query = mongodb['quartos'].find()

    quartos = json.loads(dumps(query))

    for quarto in quartos:
        query = mongodb['reservas'].find({'quarto': quarto['numero']})
        quarto['reservas'] = json.loads(dumps(query))

    return {'result': quartos}

# Listar Quarto pelo número
@quartosApp.get('/<numero>')
def getOneQuarto(mongodb, numero):
    query = mongodb['quartos'].find_one({'numero': int(numero)})
    quarto = json.loads(dumps(query))

    queryReservas = mongodb['reservas'].find({'quarto': int(numero)})
    quarto['reservas'] = json.loads(dumps(queryReservas))

    return {'result': quarto}
