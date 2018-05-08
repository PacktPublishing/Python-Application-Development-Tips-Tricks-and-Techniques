Feature: Get a list of the most interesting photos from Flickr

  Scenario: Flickr returns a correct list of photos
    Given a valid Flickr API key
    When we request a list of photos from Flickr
    Then we should receive a response of dict type
    And there should be a "photos" field in the response
    And there should be a "photo" field in response["photos"]
    And there should be a list of dicts in response["photos"]["photo"]
    And each dict in the list should contain the fields "id", "farm", "server" and "secret"
