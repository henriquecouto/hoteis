from bottle import run, route


@route('/')
def hello():
    return 'Hello, world!!!!!'


run(host='localhost', port=8080)
