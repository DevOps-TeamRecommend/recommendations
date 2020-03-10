# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Recommendation Factory to make fake recommendations for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from service.models import Recommendation


class RecommendationFactory(factory.Factory):
    """ Creates fake recommendations that you don't have to fill out """

    class Meta:
        model = Recommendation

    id = factory.Sequence(lambda n: n)
    product_1 = FuzzyInteger(1, 999) # generates a random integer between 1 and 999 to represent the id of the first product
    product_2 = FuzzyInteger(1, 999) # generates a random integer between 1 and 999 to represent the id of the second product
    recommendation_type = FuzzyChoice(choices=["upsell", "crosssell", "accessory"]) # Up-sell: more expensive version of same product, Cross sell: similar price of same product, accessory: item that goes with product
    active = FuzzyInteger(1) # 0 is FALSE and 1 is TRUE


if __name__ == "__main__":
    for _ in range(10):
        recommendation = RecommendationFactory()
        print(Recommendation.serialize())
