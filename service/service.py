"""
RECOMMENDATIONS Service

Paths:
------
GET /recommendations - Returns a list all of the Recommendations #######################
GET /recommendations/{id} - Returns the Recommendation with a given id number ##########
POST /recommendations - creates a new Recommendation record in the database ############
PUT /recommendations/{id} - updates a Recommendation record in the database ############
DELETE /recommendations/{id} - deletes a Recommendation record in the database #########

"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Recommendation, DataValidationError

# Import Flask application
from . import app

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message
        ),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            error="Method not Allowed",
            message=message,
        ),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported media type",
            message=message,
        ),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return (
        jsonify(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Internal Server Error",
            message=message,
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    # data = '{name: <string>, category: <string>}'
    # url = request.base_url + 'pets' # url_for('list_pets')
    # return jsonify(name='Pet Demo REST API Service', version='1.0', url=url, data=data), status.HTTP_200_OK
    return app.send_static_file('index.html')

######################################################################
# LIST ALL RECOMMENDATIONS
######################################################################
@app.route("/recommendations", methods=["GET"])
def list_recommendations():
    """ Returns all of the Recommendations """
    app.logger.info("Request for recommendation list")
    recommendations = []
    recommendation_type = request.args.get("recommendation_type")
    active = request.args.get("active")

    if active:   # convert to boolean
        active_bool = active.lower() in ['true', 'yes', '1']

    if recommendation_type:
        app.logger.info('Find by recommendation type: %s', recommendation_type)
        recommendations = Recommendation.find_by_recommendation_type(recommendation_type)
    elif active:
        app.logger.info('Find by active: %s', active)
        recommendations = Recommendation.find_by_active(active_bool)
    else:
        app.logger.info('Find all recs')
        recommendations = Recommendation.all()

    results = [recommendation.serialize() for recommendation in recommendations]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["GET"])
def get_recommendations(recommendation_id):
    """
    Retrieve a single recommendation
    This endpoint will return a recommendation based on it's id
    """
    app.logger.info("Request for recommendation with id: %s", recommendation_id)
    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        raise NotFound("Recommendation with id '{}' was not found.".format(recommendation_id))
    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)

# ######################################################################
# # ADD A NEW RECOMMENDATION
# ######################################################################
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
    app.logger.info('Recommendation with new id [%s] saved!', recommendation.id)
    app.logger.info(recommendation)
    # location_url  = url_for("get_recommendations", recommendation_id=recommendation.id, _external=True)
    location_url = "unimplemented"
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# UPDATE AN EXISTING RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["PUT"])
def update_recommendations(recommendation_id):
    """
    Update a Recommendation

    This endpoint will update a Recommendation based the body that is posted
    """
    app.logger.info("Request to update recommendation with id: %s", recommendation_id)
    check_content_type("application/json")
    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        raise NotFound("Recommendation with id '{}' was not found.".format(recommendation_id))
    recommendation.deserialize(request.get_json())
    recommendation.id = recommendation_id
    recommendation.save()
    app.logger.info("recommendation with id %s has been updated!", recommendation_id)
    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)

######################################################################
# DEACTIVATE AN EXISTING RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>/deactivate", methods=["PUT"])
def deactivate_recommendations(recommendation_id):
    """
    Deactivate a Recommendation

    This endpoint will deactivate a Recommendation based on the body that is posted
    """
    app.logger.info("Request to deactivate recommendation with id: %s", recommendation_id)
    check_content_type("application/json")
    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        raise NotFound("Recommendation with id '{}' was not found.".format(recommendation_id))
    recommendation.deserialize(request.get_json())
    recommendation.id = recommendation_id
    recommendation.active = 0
    recommendation.save()
    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)
    if recommendation:
        recommendation.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

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
