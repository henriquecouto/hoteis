from bottle import run, route, get

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
def getAll():
    return {'users': users}


@get('/users/<name>')
def getUser(name):
    finded_user = {}
    for user in users:
        if user['user'] == name:
            finded_user = user
    return {'user': finded_user}


if __name__ == '__main__':
    run(reloader=True, port=8080, host='localhost')
