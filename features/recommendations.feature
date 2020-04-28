Feature: The ecommerce service back-end
    As a Customer
    I want recommendations
    So that I can see similar and adjacent products incase there is a product that better suits
    my need, is cheaper, will make my experience better, or I might want to purchase in the future.


Background:
    Given the following recommendations
        | id         | product_1   | product_2   | recommendation_type | active |
        | 123        | shampoo     | hairbrush   | accessory           | True   |
        | 456        | Timex Watch | Rolex Watch | upsell              | True   |
        | 789        | roomba      | deebot      | cross sell          | False  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Pet Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Pet
    When I visit the "Home Page"
    And I set the "Name" to "Happy"
    And I set the "Category" to "Hippo"
    And I select "False" in the "Available" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Happy" in the "Name" field
    And I should see "Hippo" in the "Category" field
    And I should see "False" in the "Available" dropdown

Scenario: List all pets
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "fido" in the results
    And I should see "kitty" in the results
    And I should not see "leo" in the results

Scenario: List all dogs
    When I visit the "Home Page"
    And I set the "Category" to "dog"
    And I press the "Search" button
    Then I should see "fido" in the results
    And I should not see "kitty" in the results
    And I should not see "leo" in the results

Scenario: Update a Pet
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
    Then I should see "hairbrush" in the results
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "product_2" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see "shampoo" in the "product_1" field
    And I should see "hairbrush" in the "product_2" field
    And I should see "accessory" in the "recommendation_type" field

Scenario: Delete a recommendation
    When I visit the "Home Page"
    And I set the "recommendation_type" to "accessory"
    And I press the "Search" button
    Then I should see "hairbrush" in the results
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "product_2" field should be empty
    When I paste the "id" field
    And I press the "Delete" button
    Then I should see the message "Recommendation Successfully Deleted"
