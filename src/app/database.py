from bottle.ext.mongo import MongoPlugin

database_name = 'heroku_4q7l2460'
db_uri = 'mongodb://hoteis:oioi12@ds137336.mlab.com:37336/heroku_4q7l2460'
db_plugin = MongoPlugin(uri=db_uri, db=database_name, json_mongo=True)