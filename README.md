# Testing Instructions
### To run the automated unit tests for this application, Please execute the following command:
`python manage.py test`


# What I tested in tests.py?
1. I wrote a test to check if the Property model works properly. It makes sure that when a new property is created, it successfully links to the correct Landlord user in the database.

2. I tested the home page to make sure it actually loads without crashing (returns an HTTP 200 status) and successfully displays the property data from the database.

3. I wanted to make sure regular users can't just type the URL to see the landlord dashboard. This test pretends to be a logged-out user and checks if the system correctly blocks them and redirects them to the login page (HTTP 302).