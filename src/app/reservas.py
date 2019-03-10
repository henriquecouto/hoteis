from bottle import Bottle, request, response
from bson.json_util import dumps
import json
from database import db_plugin

reservasApp = Bottle()
reservasApp.install(db_plugin)

# Criando reserva
@reservasApp.post('/')
def createReserva(mongodb):
    newReserva = request.json
    quarto = newReserva ['quarto']

    if(quarto < 1 or quarto > 10):
        return {'result': 'Quarto não disponível'}
    
    queryCliente = mongodb['clientes'].find_one({'codigo': newReserva['cliente']})
    cliente = json.loads(dumps(queryCliente))
    if(cliente == None):
        return{'result': 'Código de cliente não cadastrado'}

    query = mongodb['reservas'].find({'quarto': quarto})

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
        try:
            mongodb['reservas'].insert(newReserva)
            return {'result': 'Reserva Criada'}
        except:
            return {'result': 'Não foi possível criar reserva'}
    else:
        return {'result': status}

# Listar Reservas
@reservasApp.get('/')
def getAllReservas(mongodb):
    query = mongodb['reservas'].find()
    reservas = dumps(query)
    return {'result': json.loads(reservas)}
