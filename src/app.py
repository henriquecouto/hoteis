from bottle import run, route, get, post, request, delete

users = [
    {
        'name': 'Henrique Couto',
        'user': 'henrique',
        'password': '123',
        'type': 'admin'
    },
    {
        'name': 'Rychard Souza',
        'user': 'rychard',
        'password': '123',
        'type': 'admin'
    },
    {
        'name': 'Fulaninho de Tal',
        'user': 'fulaninho',
        'password': '123',
        'type': 'client'
    }
]


@get('/users')
def getAllUsers():
    return {'users': users}


@get('/users/<name>')
def getUser(name):
    finded_user = {}
    for user in users:
        if user['user'] == name:
            finded_user = user
    return {'user': finded_user}


@post('/users')
def addUser():
    new_user = request.json
    users.append(new_user)
    return {'newUser': new_user}


@post('/users/<name>')
def changeUser(name):
    finded_user = {}
    for user in users:
        if user['user'] == name:
            finded_user = user
    if(finded_user):
        new_user = request.json
        users.remove(finded_user)
        users.append(new_user)
        return {'userChanged': new_user}
    else:
        return {'userChanged': 'Not finded'}


@delete('/users/<name>')
def deleteUser(name):
    finded_user = {}
    for user in users:
        if user['user'] == name:
            finded_user = user
    users.remove(finded_user)
    return {'removedUser': finded_user}


if __name__ == '__main__':
    run(reloader=True, port=8080, host='localhost')
