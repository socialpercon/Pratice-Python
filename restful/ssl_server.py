from flask import Flask
from flask.ext.restful import Api, Resource
from OpenSSL import SSL

app = Flask(__name__)
api = Api(app)

class Test(Resource):
   def get(self):
       print 'test'
       res = {'test', 'test'}
       return res

api.add_resource(Test, '/test')

if __name__ == '__main__':
   context = SSL.Context(SSL.SSLv23_METHOD)
   context.use_privatekey_file('future.key')
   context.use_certificate_file('future.crt')
   app.run(host='127.0.0.1', port=7474, debug=True, ssl_context=context)