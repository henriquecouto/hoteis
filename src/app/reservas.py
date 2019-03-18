from bottle import Bottle, request, response
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from database import db_plugin

reservasApp = Bottle()
reservasApp.install(db_plugin)

# Criando reserva
@reservasApp.post('/')
def createReserva(mongodb):
    newReserva = request.json
    quarto = newReserva['quarto']

    if(quarto < 1 or quarto > 10):
        return {'result': 'Quarto não disponível'}

    queryCliente = mongodb['clientes'].find_one(
        {'codigo': newReserva['cliente']})
    cliente = json.loads(dumps(queryCliente))
    if(cliente == None):
        return{'result': 'Código de cliente não cadastrado'}

    queryQuarto = mongodb['quartos'].find_one({'numero': quarto})
    limite = json.loads(dumps(queryQuarto))['capacidade']

    if(limite < newReserva['hospedes']):
        return {'result': 'Capacidade excedida!!!'}

    query = mongodb['reservas'].find({'quarto': quarto})

    reservas = dumps(query)

    disponivel = True
    status = 'Reserva Disponível'

    if(newReserva['saida'] < newReserva['entrada']):
        return {'result': 'A data de entrada deve ser antes da data de saída'}
    else:
        for reserva in json.loads(reservas):
            if (reserva['saida'] >= newReserva['entrada']) and (reserva['entrada'] <= newReserva['saida']):
                disponivel = False
                status = 'Reserva não disponível'

    newReserva['status'] = 'Aguardando'

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

# Cancelar reservas
# @reservasApp.delete('/')
# def deleteReserva(mongodb):

#     id = request.json['$oid']

#     try:
#         mongodb['reservas'].delete_one({'_id':ObjectId(id)})
#         return {'result':'Reserva Cancelada!!'}
#     except:
#         return {'result':'Erro ao Cancelar Reserva!!'}

# Check-in Check-out
@reservasApp.put('/')
def changeReservaStatus(mongodb):
    alteracoes = request.json['alteracoes']
    reserva_id = ObjectId(request.json['_id'])

    queryReserva = mongodb['reservas'].find_one({'_id': reserva_id})
    reserva = json.loads(dumps(queryReserva))

    queryQuarto = mongodb['quartos'].find_one({'numero': reserva['quarto']})
    quarto = json.loads(dumps(queryQuarto))

    if(alteracoes['status']=='Check-In'):
        if (alteracoes['hospedes'] > quarto['capacidade']):
            return {'result': False, 'message': 'Capacidade Excedida'}

    if(alteracoes['status'] == 'Check-Out'):

        if(reserva['entrada'] > alteracoes['saida']):
            return {'result': False, 'message': 'A data de Check-Out não pode ser antes da data de Check-In'}

        adicional = 0
        if(reserva['hospedes'] > quarto['capacidade'] - 1):
            adicional = 30

        valor = ((alteracoes['saida'] - reserva['entrada'])*quarto['diaria'])
        alteracoes['valor'] = valor + valor * (adicional/100)

    try:
        mongodb['reservas'].update_one(
            {'_id': reserva_id},
            {'$set': alteracoes})
        return {'result': True}
    except:
        return {'result': False}
