Feature: The ecommerce service back-end
    As a Customer
    I want recommendations
    So that I can see similar and adjacent products incase there is a product that better suits
    my need, is cheaper, will make my experience better, or I might want to purchase in the future.


Background:
    Given the following recommendations
        | product_1   | product_2   | recommendation_type | active |
        | 10001       | 10002       | accessory           | True   |
        | 42001       | 42002       | upsell              | True   |
        | 31001       | 31001       | cross sell          | False  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Recommendation Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set the "product_1" to "10001"
    And I set the "product_2" to "10002"
    And I set the "recommendation_type" to "accessory"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "product_1" field should be empty
    And the "product_2" field should be empty
    And the "recommendation_type" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "f" in the "product_1" field
    And I should see "10002" in the "product_2" field
    And I should see "accessory" in the "recommendation_type" field 
    And I should see "True" in the "active" dropdown


Scenario: List all recommendations
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "10001" in the results
    And I should see "31001" in the results
    And I should not see "23001" in the results

Scenario: List all accessories
    When I visit the "Home Page"
    And I set the "recommendation_type" to "accessory"
    And I press the "Search" button
    Then I should see "10001" in the results
    And I should not see "31001" in the results
    And I should not see "42001" in the results

Scenario: Update a Recommendation
    When I visit the "Home Page"
    And I set the "Name" to "fido"
    And I press the "Search" button
    Then I should see "fido" in the "Name" field
    And I should see "dog" in the "Category" field
    When I change "Name" to "Boxer"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Boxer" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "Boxer" in the results
    Then I should not see "fido" in the results

Scenario: Read a recommendation
    When I visit the "Home Page"
    And I set the "recommendation_type" to "accessory"
    And I press the "Search" button
    Then I should see "10002" in the results
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "product_2" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "10001" in the "product_1" field
    And I should see "10002" in the "product_2" field
    And I should see "accessory" in the "recommendation_type" field

Scenario: Delete a recommendation
    When I visit the "Home Page"
    And I set the "recommendation_type" to "accessory"
    And I press the "Search" button
    Then I should see "10002" in the results
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "product_2" field should be empty
    When I paste the "id" field
    And I press the "Delete" button
    Then I should see the message "Recommendation Successfully Deleted"
