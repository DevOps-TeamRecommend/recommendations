"""
Recommendation API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import json
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db
from service.service import app, init_db

from .factories import RecommendationFactory

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

# GET DATABASE SETUP FOR LOCAL OR PROD
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap['user-provided'][0]['credentials']['url']

######################################################################
#  T E S T   C A S E S
######################################################################
class TestRecommendationServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()


    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E
######################################################################
    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        #self.assertEqual(data["name"], "Recommendation Demo REST API Service")

    def _create_recommendations(self, count):
        """ Factory method to create recommendations in bulk """
        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationFactory()
            resp = self.app.post(
                "/recommendations", json=test_recommendation.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test recommendation"
            )
            new_recommendation = resp.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)
        return recommendations

    def test_get_recommendation_list(self):
        """ Get a list of Recommendations """
        self._create_recommendations(5)
        resp = self.app.get("/recommendations")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)


    def test_query_by_recommendation_type(self):
        """ Query Recommendations by type """
        self._create_recommendations(20)
        resp = self.app.get('/recommendations', query_string='recommendation_type=upsell')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertIn(b'upsell', resp.data)
        self.assertNotIn(b'accessory', resp.data)
        data = resp.get_json()
        logging.debug('data = %s', data)
        query_item = data[0]
        self.assertEqual(query_item['recommendation_type'], 'upsell')

    def test_query_by_active(self):
        """ Query Recommendations by active status """
        self._create_recommendations(20)
        resp = self.app.get('/recommendations', query_string='active=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertIn(b'true', resp.data)
        self.assertNotIn(b'false', resp.data)
        data = resp.get_json()
        logging.debug('data = %s', data)
        query_item = data[0]
        self.assertEqual(query_item['active'], True)

    def test_get_recommendation(self):
        """ Get a single Recommendation """
        # get the id of a recommendation
        test_recommendation = self._create_recommendations(1)[0]
        resp = self.app.get(
            "/recommendations/{}".format(test_recommendation.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], test_recommendation.id)

    def test_get_recommendation_not_found(self):
        """ Get a Recommendation thats not found """
        resp = self.app.get("/recommendations/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recommendation(self):
        """ Create a new recommendation """
        test_recommendation = RecommendationFactory()
        resp = self.app.post(
            "/recommendations", json=test_recommendation.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_recommendation = resp.get_json()
        self.assertEqual(new_recommendation["product_1"], test_recommendation.product_1, "Product_1s do not match")
        self.assertEqual(
            new_recommendation["product_2"], test_recommendation.product_2, "Product_2s do not match"
        )
        self.assertEqual(new_recommendation["recommendation_type"], test_recommendation.recommendation_type, "Recommendation Types do not match")
        self.assertEqual(
            new_recommendation["active"], test_recommendation.active, "Status does not match"
        )
        # TODO: Uncomment these and update attributes when location header is implemented
        # Check that the location header was correct
        # resp = self.app.get(location, content_type="application/json")
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # new_recommendation = resp.get_json()
        # self.assertEqual(new_recommendation["name"], test_recommendation.name, "Names do not match")
        # self.assertEqual(
        #     new_recommendation["category"], test_recommendation.category, "Categories do not match"
        # )
        # self.assertEqual(
        #     new_recommendation["available"], test_recommendation.available, "Availability does not match"
        # )

    def test_update_recommendation(self):
        """ Update an existing Recommendation """
        # create a recommendation to update
        test_recommendation = RecommendationFactory()
        resp = self.app.post(
            "/recommendations", json=test_recommendation.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the recommendation
        new_recommendation = resp.get_json()
        new_recommendation["active"] = False
        resp = self.app.put(
            "/recommendations/{}".format(new_recommendation["id"]),
            json=new_recommendation,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_recommendation = resp.get_json()
        self.assertEqual(updated_recommendation["active"], False)


    def test_deactivate_recommendation(self):
        """ Deactivate an existing Recommendation """
        # create a recommendation to deactivate
        test_recommendation = RecommendationFactory()
        resp = self.app.post(
            "/recommendations", json=test_recommendation.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # deactivate the recommendation
        new_recommendation = resp.get_json()
        resp = self.app.put(
            "/recommendations/{}/deactivate".format(new_recommendation["id"]),
            json=new_recommendation,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_recommendation = resp.get_json()
        self.assertEqual(updated_recommendation["active"], False)


    def test_bad_content_type(self):
        """ Create a recommendation with a bad content type """
        test_recommendation = RecommendationFactory()
        resp = self.app.post(
            "/recommendations", json=test_recommendation.serialize(), content_type="wrong"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_delete_recommendation(self):
        """ Delete a recommendation """
        test_recommendation = self._create_recommendations(1)[0]
        resp = self.app.delete(
            "/recommendations/{}".format(test_recommendation.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        # TODO: uncomment this code when get is implemented
        # resp = self.app.get(
        #     "/recommendations/{}".format(test_recommendation.id), content_type="application/json"
        # )
        # self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
