import unittest
import sys
sys.path.append('.')  # Add the current directory to the system path
from flask_app.app import app  # Import the Flask app from the folder
class FlaskAppTests(unittest.TestCase):
    # Set up the test client
    def setUp(self):
        self.app = app.test_client()  # Use the Flask test client
        self.app.testing = True  # Enable testing mode

    # Test the home page (root URL)
    def test_home_page(self):
        response = self.app.get('/')  # Simulate a GET request to the home page
        self.assertEqual(response.status_code, 200)  # Check if the status code is 200 (OK)
        self.assertIn(b'This is how i Deploy a Containerized Flask Application to AWS EKS using Terraform! - Sam In The Cloud', response.data)  # Check if the expected message is in the response

    # Clean up after tests (if necessary)
    def tearDown(self):
        pass  # Clean up resources after each test

if __name__ == '__main__':
    unittest.main()
