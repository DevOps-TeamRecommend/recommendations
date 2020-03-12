"""
Models for Recommendation

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Recommendation(db.Model):
    """
    Class that represents a Recommendation
    """

    app = None

    # RECOMMENDATION Table Schema
    # each recommendation will hhve the following fields:
    id = db.Column(db.Integer, primary_key=True) # id of this particular recommendation
    product_1 = db.Column(db.Integer) # id of first product
    product_2 = db.Column(db.Integer) # id of second product
    recommendation_type = db.Column(db.String(63)) # Up-sell: more expensive version of same product, Cross sell: similar price of same product, accessory: item that goes with product
    active = db.Column(db.Boolean) # Whether recommendation still exists or was removed


    # DEV
    def __repr__(self):
        return "Recommendation id=[%s]>" % (self.id)

    # AJ
    def create(self):
        """
        Creates a recommendation to the database
        """
        logger.info("Creating %s", self.id)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a recommendation to the database
        """
        logger.info("Saving %s", self.id)
        db.session.commit()

    # AJ
    def delete(self):
        """ Removes a recommendation from the data store """
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    # AJ
    def serialize(self):
        """ Serializes a recommendation into a dictionary """
        return {
            "id": self.id,
            "product_1": self.product_1,
            "product_2": self.product_2,
            "recommendation_type": self.recommendation_type,
            "active": self.active,
        }

    # AJ
    def deserialize(self, data):
        """
        Deserializes a recommendation from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.product_1 = data["product_1"]
            self.product_2 = data["product_2"]
            self.recommendation_type = data["recommendation_type"]
            self.active = data["active"]
        except KeyError as error:
            raise DataValidationError("Invalid recommendation: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid recommendation: body of request contained" "bad or no data"
            )
        return self

    #######################################################################
    # EVERYTHING BELOW HERE HAS BEEN UPDATED BY DEVNEEL - ALREADY COMPLETE
    ######################################################################

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

#this is the list fuction
    @classmethod
    def all(cls):
        """ Returns all of the Recommendations in the database """
        logger.info("Processing all Recommendations")
        return cls.query.all()

# GEORGE - These are complete but they are part of the read story
    @classmethod
    def find(cls, id):
        """ Finds a recommendation by it's ID """
        logger.info("Processing lookup for id %s ...", id)
        return cls.query.get(id)

    @classmethod
    def find_or_404(cls, id):
        """ Find a recommendation by it's id """
        logger.info("Processing lookup or 404 for id %s ...", id)
        return cls.query.get_or_404(id)

#CLAIRE
    @classmethod
    def find_by_active(cls, active):
        """ Returns all recommendations with the given active status

        Args:
            active (integer): the recommendation's active status (0 for inactive and 1 for active)
        """
        logger.info("Processing active status query for %s ...", active)
        return cls.query.filter(cls.active == active)

    @classmethod
    def find_by_product_1(cls, product_1):
        """ Returns all recommendations with product_1

        Args:
            product_1 (integer): the id of the first product
        """
        logger.info("Processing product_id query for %s ...", product_1)
        return cls.query.filter(cls.product_1 == product_1)

    @classmethod
    def find_by_product_2(cls, product_2):
        """ Returns all recommendations with product_2

        Args:
            product_2 (integer): the id of the second product
        """
        logger.info("Processing product_id query for %s ...", product_2)
        return cls.query.filter(cls.product_2 == product_2)


    @classmethod
    def find_by_recommendation_type(cls, recommendation_type):
        """ Returns all of the recommnedations of specified type (upsell, cross_sell, accessory)

        Args:
            recommendation_type (string): the recommendation_type of the two products
        """
        logger.info("Processing recommendation_type query for %s ...", recommendation_type)
        return cls.query.filter(cls.recommendation_type == recommendation_type)
