from bottle import Bottle
import json
from bottle.ext.mongo import MongoPlugin

app = Bottle()
database_name = 'heroku_4q7l2460'
db_uri = 'mongodb://hoteis:oioi12@ds137336.mlab.com:37336/heroku_4q7l2460'
db_plugin = MongoPlugin(uri=db_uri,db=database_name)

app.install(db_plugin)

@app.route('/users')
def getAll(mongodb):
    query = mongodb['users'].find()
    results = []
    for q in query:
        results.append(q['user'])
    return {'result':results}

@app.route('/users/<name>')
def getOne(mongodb,name):
    query = mongodb['users'].find({'user':name})
    result = []
    for q in query:
        result.append(q['user'])
    return {'result':result}

if __name__ == '__main__':
    app.run(debug=True,reloader=True, port=8080,host='localhost')
