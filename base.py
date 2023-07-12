from flask import Flask, send_from_directory
from flask import jsonify, request
import os
from flask_cors import CORS, cross_origin
from config import app, con
from flask_swagger_ui import get_swaggerui_blueprint
from routes.datatable import *

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'My API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    return send_from_directory('static', 'swagger.json')

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)