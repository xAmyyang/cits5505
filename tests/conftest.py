import sys
import os
import pytest

# Add project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


# This fixture creates a test client for the Flask app.
# The client can be used to send requests to routes
# without running the actual server.
@pytest.fixture
def client():

    # Enable testing mode
    app.config["TESTING"] = True

    # Create test client
    with app.test_client() as client:
        yield client