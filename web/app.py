from flask import Flask, render_template, Blueprint, url_for
from flask import request
from flask import json
from flask import Response
from flask import jsonify
from flask.ext.restplus import Api, Resource, apidoc
import pprint
import initSearch
app = Flask(__name__)

blueprint = Blueprint('api', __name__)
api = Api(blueprint, title='Tasks API', ui=False)
createParser = api.parser()
createParser.add_argument('query', type=str)
createParser.add_argument('command', type=str)

# print(initSearch.getterms())
@api.route('/')
class Index(Resource):
    @api.doc(parser=createParser)
    def post(self):
        """
        depends on what is request is
        command or search call
        appropriate method
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
