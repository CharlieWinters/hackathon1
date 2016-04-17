from flask import Flask, jsonify, Response
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
from suds.client import Client
import logging
import datetime
import json
from flask_cors import CORS

port = os.getenv('PORT', '4999')
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
CORS(app)
admin = Admin(app, name='pingins', template_mode='bootstrap3')
app.secret_key='daahackathon'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.TEXT)
    balance = db.Column(db.REAL)
    parking = db.Column(db.BOOLEAN)
    checkin = db.Column(db.BOOLEAN)
    security = db.Column(db.BOOLEAN)
    shopping = db.Column(db.BOOLEAN)
    departure = db.Column(db.BOOLEAN)

db.create_all()

admin.add_view(ModelView(User, db.session))
api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT'])

username = 'headbroken'
apiKey = '2428b712a94d4e1489340da6da32625791ad6e8d'
url = 'http://flightxml.flightaware.com/soap/FlightXML2/wsdl'

# This is a custom HTTP transport that allows Basic Authentication.
logging.basicConfig(level=logging.INFO)
api = Client(url, username=username, password=apiKey)

@app.route("/flightapi")
def hello():

    # print api

    # Get the weather
    result = api.service.Metar('KAUS')

    # Get the flights enroute
    result = api.service.Scheduled('EIDW', 30, '', 0)
    flights = result['scheduled']
    flightlisting = []
    # flightdict = {}
    # flightsdict = {}
    for flight in flights:
        flightdict = {}
        flightdict['flightnumber'] = flight['ident']
        flightdict['destinationName'] =flight['destinationName']
        flightdict['estimatedarrivaltime'] = flight['estimatedarrivaltime']
        flightdict['filed_departuretime'] = flight['filed_departuretime']
        #flightsdict[flight['ident']] = flightdict
        flightlisting.append(flightdict)
    # flightlisting.append(flightsdict)
    resp = Response(response=json.dumps(flightlisting),
                    status=200,
                    mimetype="application/json")
    return resp

if __name__ == "__main__":
    app.run('0.0.0.0', port=int(port))
