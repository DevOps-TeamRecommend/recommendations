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
    active = db.Column(db.Integer) # 0 is FALSE and 1 is TRUE


    # DEV
    def __repr__(self):
        return "Recommendation id=[%s]>" % (self.id)

    # GEORGE
    def create(self):
        """
        Creates a <your resource name> to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    # GEORGE
    def save(self):
        """
        Updates a <your resource name> to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    # AJ
    def delete(self):
        """ Removes a <your resource name> from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    # CLAIRE
    def serialize(self):
        """ Serializes a <your resource name> into a dictionary """
        return {
            "id": self.id,
            "name": self.name
        }

    # CLAIRE
    def deserialize(self, data):
        """
        Deserializes a <your resource name> from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
        except KeyError as error:
            raise DataValidationError("Invalid <your resource name>: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid <your resource name>: body of request contained" "bad or no data"
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

    @classmethod
    def all(cls):
        """ Returns all of the Recommendations in the database """
        logger.info("Processing all Recommendations")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a recommendation by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a recommendation by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_active(cls, active):
        """ Returns all recommendations with the given active status

        Args:
            active (integer): the recommendation's active status (0 for inactive and 1 for active)
        """
        logger.info("Processing active status query for %s ...", active)
        return cls.query.filter(cls.active == active)
