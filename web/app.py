from flask import Flask, render_template, Blueprint, url_for
from flask import request
from flask import json
from flask import Response
from flask import jsonify
from flask.ext.restplus import Api, Resource, apidoc
import initSearch
app = Flask(__name__)

blueprint = Blueprint('api', __name__)
api = Api(blueprint, title='Tasks API', ui=False)
createParser = api.parser()
createParser.add_argument('query', type=str)
createParser.add_argument('command', type=str)


@api.route('/')
class Index(Resource):
    @api.doc(parser=createParser)
    def post(self):
        """
        Create new task
        """
        args = createParser.parse_args()
        print(args['command'])
        print(args['query'])
        if args['command'] != None:
            method = getattr(initSearch, str(args['command']))
            result = method()
        else:
            result = initSearch.startSearch(str(args['query']))
        resp = jsonify(result)
        resp.status_code = 200
        return resp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello')
def hello():
    return render_template('hello.html')

app.register_blueprint(blueprint)
if __name__ == '__main__':
    app.run(debug=True)

#
# @app.route('/articles/<articleid>')
# def api_article(articleid):
#     return 'You are reading ' + articleid
#
#
# @app.route('/articles')
# def api_articles():
#     if 'name' in request.args:
#         return 'Hello ' + request.args['name']
#     else:
#         return 'Hello John Doe'
#
#
# @app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
# def api_echo():
#     if request.method == 'GET':
#         return "ECHO: GET\n"
#
#     elif request.method == 'POST':
#         return "ECHO: POST\n"
#
#     elif request.method == 'PATCH':
#         return "ECHO: PACTH\n"
#
#     elif request.method == 'PUT':
#         return "ECHO: PUT\n"
#
#     elif request.method == 'DELETE':
#         return "ECHO: DELETE"
#
#
# @app.route('/messages', methods = ['POST'])
# def api_message():
#
#     if request.headers['Content-Type'] == 'text/plain':
#         return "Text Message: " + request.data
#
#     elif request.headers['Content-Type'] == 'application/json':
#         print(request.data)
#         return "JSON Message: " + json.dumps(request.json)
#
#     elif request.headers['Content-Type'] == 'application/octet-stream':
#         f = open('./binary', 'wb')
#         f.write(request.data)
#         f.close()
#         return "Binary message written!"
#     else:
#         return "415 Unsupported Media Type ;)"
#
#
# @app.route('/hello2', methods = ['GET'])
# def api_hello():
#     data = {
#         'hello': 'world',
#         'number': 3
#     }
#     js = json.dumps(data)
#
#     resp = jsonify(data)
#     resp.status_code = 200
#     resp.headers['Link'] = 'http://luisrei.com'
#
#     return resp
