import unittest
import json
from app import create_app

class TestEndpoints(unittest.TestCase):
    """
    Refactored test class to fix dependency issues and assertion failures 
    by using setUpClass to create required entities.
    """

    @classmethod
    def setUpClass(cls):
        """Setup client and create essential entities (User, Place, Amenity) once."""
        # 1. Setup client
        app = create_app()
        app.config['TESTING'] = True
        cls.client = app.test_client()
        cls.base_url = '/api/v1/'
        
        # 2. Create required entities (Dependencies for other tests)

        # Create User
        user_data = {"email": "setup@user.com", "first_name": "Setup", "last_name": "User"}
        user_response = cls.client.post(cls.base_url + 'users/', json=user_data)
        cls.USER_ID = json.loads(user_response.data).get('id')
        
        # Create Amenity
        amenity_data = {"name": "Test Amenity"}
        amenity_response = cls.client.post(cls.base_url + 'amenities/', json=amenity_data)
        cls.AMENITY_ID = json.loads(amenity_response.data).get('id')

        # Create Place (requires USER_ID)
        place_data = {
            "title": "Valid Place", "description": "Desc", "price": 100.0, 
            "latitude": 45.0, "longitude": 45.0, 
            "owner_id": cls.USER_ID, "amenities": []
        }
        place_response = cls.client.post(cls.base_url + 'places/', json=place_data)
        cls.PLACE_ID = json.loads(place_response.data).get('id')
        
        # Create Review (requires USER_ID and PLACE_ID)
        review_data = {
            "text": "Great stay", "rating": 5.0, 
            "user_id": cls.USER_ID, "place_id": cls.PLACE_ID
        }
        review_response = cls.client.post(cls.base_url + 'reviews/', json=review_data)
        cls.REVIEW_ID = json.loads(review_response.data).get('id')

    # --- USER ENDPOINTS ---

    def test_01_create_user_success(self):
        """Test user creation with valid data (201)."""
        response = self.client.post(self.base_url + 'users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe2@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_02_create_user_invalid_email(self):
        """Test user creation with invalid email format (400)."""
        response = self.client.post(self.base_url + 'users/', json={
            "first_name": "Test",
            "last_name": "Fail",
            "email": "invalid-email" # Missing @-sign
        })
        self.assertEqual(response.status_code, 400)
        # FIX: Assert against the actual message returned by the API
        self.assertIn("An email address must have an @-sign", str(response.data))

    # --- AMENITY ENDPOINTS ---
    
    def test_03_create_amenity_success(self):
        """Test amenity creation with valid data (201)."""
        response = self.client.post(self.base_url + 'amenities/', json={"name": "New Amenity"})
        self.assertEqual(response.status_code, 201)

    # --- PLACE ENDPOINTS ---

    def test_04_create_place_invalid_latitude(self):
        """Test place creation with latitude outside boundary (400)."""
        # FIX: Uses self.USER_ID from setUpClass to satisfy the dependency check
        response = self.client.post(self.base_url + 'places/', json={
            "title": "Bad Lat", "price": 10.0, 
            "latitude": 90.1,  # Out of range, should trigger model validation
            "longitude": 45.0, 
            "owner_id": self.USER_ID, 
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
        # FIX: Asserts against the model validation message
        self.assertIn("latitude must be between -90 and 90", str(response.data))

    # --- REVIEW ENDPOINTS ---

    def test_05_create_review_invalid_rating(self):
        """Test review creation with rating outside boundary (400)."""
        # FIX: Uses self.USER_ID and self.PLACE_ID from setUpClass
        response = self.client.post(self.base_url + 'reviews/', json={
            "text": "Too high", "rating": 10.0, # Out of range
            "user_id": self.USER_ID, 
            "place_id": self.PLACE_ID
        })
        self.assertEqual(response.status_code, 400)
        # FIX: Asserts against the model validation message
        self.assertIn("rating must be between 1 and 5", str(response.data))

if __name__ == '__main__':
    unittest.main()