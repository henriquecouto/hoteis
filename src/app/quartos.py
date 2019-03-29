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

# Número Quartos de Ocupados
@quartosApp.get('/ocupados')
def getOcupados(mongodb):
    query = mongodb['reservas'].find({'status': 'Check-In'})
    ocupados = len(json.loads(dumps(query)))

    return {'result': ocupados}

# Buscar Quartos
@quartosApp.get('/search/<search>')
def searchQuartos(mongodb, search):
    if search.isdigit():
        query = mongodb['quartos'].find({'numero': int(search)})
    else:
        query = mongodb['quartos'].find({'tipo': {'$regex': f'^{search}', '$options': 'i'}})
    
    qrts = json.loads(dumps(query))

    for qrt in qrts:
        queryRes = mongodb['reservas'].find({'quarto': int(qrt['numero'])})
        qrt['reservas'] = json.loads(dumps(queryRes))

    return {'result': qrts}

# Tá ocupado?
@quartosApp.get('/ocupado/<number>')
def isOcuped(mongodb, number):
    result = 'Não'

    query = mongodb['reservas'].find_one({'quarto': int(number), 'status': 'Check-In'})
    reserva = json.loads(dumps(query))
    if reserva:
        result = 'Sim'

    return {'result': result}