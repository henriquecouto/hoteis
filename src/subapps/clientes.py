from bottle import Bottle, request, response
from bson.json_util import dumps
import json
from database import db_plugin

clientesApp = Bottle()
clientesApp.install(db_plugin)


# Listar Clientes
@clientesApp.route('/')
def getAllClientes(mongodb):
    query = mongodb['clientes'].find()

    clientes = json.loads(dumps(query))

    for cliente in clientes:
        query = mongodb['reservas'].find({'cliente': cliente['codigo']})
        cliente['reservas'] = json.loads(dumps(query))

    return {'result': clientes}

# Buscar Cliente
@clientesApp.route('/<nome>')
def getCliente(mongodb, nome):
    query = mongodb['clientes'].find({'nome': {'$regex': f'^{nome}', '$options': 'i'}})
    clientes = json.loads(dumps(query))

    for cliente in clientes:
        queryReservas = mongodb['reservas'].find({'cliente': cliente['codigo']})
        cliente['reservas'] = json.loads(dumps(queryReservas))

    return{'result': clientes}

# Cadastrar Cliente
@clientesApp.route('/', method='POST')
def addCliente(mongodb):
    newUser = request.json
    query = mongodb['clientes'].find_one({'codigo': newUser['codigo']})

    oldUser = json.loads(dumps(query))

    if(oldUser == None):
        try:
            mongodb['clientes'].insert(newUser)
            return {'result': 'Cliente cadastrado com sucesso!'}
        except:
            return {'result': 'Não foi possível cadastrar o cliente'}
    else:
        return {'result': 'Código de usuário não disponível'}

# Alterar Cliente
@clientesApp.route('/<codigo>', method='PUT')
def changeCliente(mongodb, codigo):
    newUser = request.json

    if 'codigo' in newUser:
        return {'result': 'Não é possível alterar o código do cliente'}

    query = mongodb['clientes'].find_one({'codigo': int(codigo)})

    oldUser = json.loads(dumps(query))

    if(oldUser == None):
        return {'result': 'Código de usuário não cadastrado'}
    else:
        mongodb['clientes'].update_one(
            {'codigo': int(codigo)}, {"$set": newUser})
        return {'result': 'Usuário atualizado'}
