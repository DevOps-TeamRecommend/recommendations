"""
Test cases for Recommendations Model

"""
import logging
import unittest
import os
from werkzeug.exceptions import NotFound
from service.models import Recommendation, DataValidationError, db
from service import app
from .factories import RecommendationFactory

# ADDED BY DEV
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  Recommendation   M O D E L   T E S T   C A S E S
######################################################################
class TestRecommendation(unittest.TestCase):
    """ Test Cases for Recommendation Model """

    # DEV _ COMPLETE
    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Recommendation.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E
######################################################################

    def test_create_a_recommendation(self):
        """ Create a recommendation and assert that it exists """
        recommendation = Recommendation(product_1=100, product_2=200, recommendation_type="accessory", active=True)
        self.assertTrue(recommendation != None)
        self.assertEqual(recommendation.id, None)
        self.assertEqual(recommendation.product_1, 100)
        self.assertEqual(recommendation.product_2, 200)
        self.assertEqual(recommendation.recommendation_type, "accessory")
        self.assertEqual(recommendation.active, True)
        recommendation = Recommendation(product_1=100, product_2=200, recommendation_type="accessory", active=False)
        self.assertEqual(recommendation.active, False)

    def test_add_a_recommendation(self):
        """ Create a recommendation and add it to the database """
        recommendations = Recommendation.all()
        self.assertEqual(recommendations, [])
        recommendation = Recommendation(product_1=100, product_2=200, recommendation_type="accessory", active=True)
        self.assertTrue(recommendation != None)
        self.assertEqual(recommendation.id, None)
        recommendation.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(recommendation.id, 1)
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 1)

    def test_delete_a_recommendation(self):
        """ Delete a Recommendation """
        recommendation = RecommendationFactory()
        recommendation.create()
        self.assertEqual(len(recommendation.all()), 1)
        # delete the recommendation and make sure it isn't in the database
        recommendation.delete()
        self.assertEqual(len(recommendation.all()), 0)

    def test_serialize_a_recommendation(self):
        """ Test serialization of a Recommendation """
        recommendation = RecommendationFactory()
        data = recommendation.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], recommendation.id)
        self.assertIn("product_1", data)
        self.assertEqual(data["product_1"], recommendation.product_1)
        self.assertIn("product_2", data)
        self.assertEqual(data["product_2"], recommendation.product_2)
        self.assertIn("recommendation_type", data)
        self.assertEqual(data["recommendation_type"], recommendation.recommendation_type)
        self.assertIn("active", data)
        self.assertEqual(data["active"], recommendation.active)

    def test_deserialize_a_recommendation(self):
        """ Test deserialization of a recommendation """
        data = {"id": 1, "product_1": 100, "product_2": 200, "recommendation_type": "accessory", "active": True}
        recommendation = RecommendationFactory()
        recommendation.deserialize(data)
        self.assertNotEqual(recommendation, None)
        self.assertEqual(recommendation.id, 1)
        self.assertEqual(recommendation.product_1, 100)
        self.assertEqual(recommendation.product_2, 200)
        self.assertEqual(recommendation.recommendation_type, "accessory")
        self.assertEqual(recommendation.active, True)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        Recommendation = RecommendationFactory()
        self.assertRaises(DataValidationError, Recommendation.deserialize, data)

#CLAIRE
    def test_find_by_recommendation_type(self):
        """ Find recommendation by recommendation_type """
        Recommendation(id=1, product_1=200, product_2=300, recommendation_type = "upsell", active = True).create()
        Recommendation(id=2, product_1=300, product_2=400, recommendation_type = "crosssell", active = True).create()
        recommendations = Recommendation.find_by_recommendation_type("upsell")

    def test_find_by_id(self):
        """ Find recommendation by id """
        Recommendation(id=10, product_1=205, product_2=310, recommendation_type = "upsell", active = True).create()
        Recommendation(id=20, product_1=305, product_2=405, recommendation_type = "crosssell", active = True).create()
        recommendations = Recommendation.find(10)


    def test_find_by_product_1(self):
        """ Find recommendation by product_1 id """
        Recommendation(id=3, product_1=400, product_2=600, recommendation_type = "upsell", active = True).create()
        Recommendation(id=4, product_1=500, product_2=700, recommendation_type = "crosssell", active = True).create()
        recommendation = Recommendation.find_by_product_1(400)


    def test_find_by_product_2(self):
        """ Find recommendation by product_2 id """
        Recommendation(id=5, product_1=700, product_2=900, recommendation_type = "upsell", active = True).create()
        Recommendation(id=6, product_1=800, product_2=901, recommendation_type = "crosssell", active = True).create()
        recommendation = Recommendation.find_by_product_2(901)


    def test_find_by_active(self):
        """ Find recommendation by active status """
        Recommendation(id=7, product_1=705, product_2=905, recommendation_type = "upsell", active = False).create()
        Recommendation(id=8, product_1=805, product_2=910, recommendation_type = "crosssell", active = True).create()
        recommendation = Recommendation.find_by_active(False)


    def test_find_or_404_found(self):
        """ Find or return 404 found """
        recommendations = RecommendationFactory.create_batch(3)
        for Recommendation in recommendations:
            Recommendation.create()

        recommendation = Recommendation.find_or_404(recommendations[1].id)


    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, Recommendation.find_or_404, 0)
