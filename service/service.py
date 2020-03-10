"""
RECOMMENDATIONS Service

Paths:
------
GET /recommendation - Returns a list all of the Recommendations ######################## CLAIRE - TODO
GET /recommendations/{id} - Returns the Recommendation with a given id number ########## CLAIRE - TODO
POST /recommendations - creates a new Recommendation record in the database ############ GEORGE - TODO
PUT /recommendations/{id} - updates a Recommendation record in the database ############ DEV - TODO
DELETE /recommendations/{id} - deletes a Recommendation record in the database ######### AJ - TODO

"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Recommendation, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return "Reminder: return some useful information in json format about the service here", status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Recommendation.init_db(app)
