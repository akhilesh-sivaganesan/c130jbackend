from flask import Flask
from flask_cors import CORS
import sqlalchemy

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

host = 'aero-webapps.cnh4wzlssbju.us-gov-west-1.rds.amazonaws.com'
database = 'osf'
username = 'osf_data_team'
password = 'Data4Life135!'
port = '5432'
engine = sqlalchemy.create_engine(
    f'postgresql://{username}:{password}@{host}:{port}/{database}')
con = engine.connect()
