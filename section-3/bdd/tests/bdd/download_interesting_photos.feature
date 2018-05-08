Feature: Download 100 interesting photos from Flickr


  Scenario: Flickr sends out 100 interesting photos
    Given a valid Flickr API key and a valid download directory
    When we request to download 100 interesting photos from Flickr
    Then the download directory should contain 100 files
    And all the file names in the download directory should end with ".jpg"
