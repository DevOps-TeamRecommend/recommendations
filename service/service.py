"""
RECOMMENDATIONS Service

Paths:
------
GET /recommendations - Returns a list all of the Recommendations ######################## CLAIRE - TODO
GET /recommendations/{id} - Returns the Recommendation with a given id number ########## GEORGE - TODO
POST /recommendations - creates a new Recommendation record in the database ############ AJ - TODO
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
    return (
        jsonify(
            name="Recommendation Demo REST API Service",
            version="1.0"
        ),
        status.HTTP_200_OK,
    )
            # TODO: UNCOMMENT this when list_recommendation is written
            # paths=url_for("list_recommendations", _external=True),

######################################################################
# ADD A NEW RECOMMENDATION
######################################################################
@app.route("/recommendations", methods=["POST"])
def create_recommendations():
    """
    Creates a recommendation
    This endpoint will create a recommendation based the data in the body that is posted
    """
    app.logger.info("Request to create a recommendation")
    check_content_type("application/json")
    recommendation = Recommendation()
    recommendation.deserialize(request.get_json())
    recommendation.create()
    message = recommendation.serialize()
    # TODO: uncomment this next line one get_recommendations is written
    # location_url = url_for("get_recommendations", recommendation_id=recommendation.id, _external=True)
    # TODO: remove line below when get_recommendations is written
    location_url = "unimplemented"
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# DELETE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["DELETE"])
def delete_recommendations(recommendation_id):
    """
    Delete a recommendation

    This endpoint will delete a recommendation based the id specified in the path
    """
    app.logger.info("Request to delete recommendation with id: %s", recommendation_id)
    recommendation = Recommendation.find(recommendation_id)
    if recommendation:
        recommendation.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Recommendation.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return 
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))
