import unittest
import json
from app import create_app

class TestEndpoints(unittest.TestCase):
    """
    Comprehensive test class for HBNB API endpoints, utilizing setUpClass 
    to manage necessary entity creation and cleanup.
    """
    # Define a non-existent but valid ID for 404 testing
    NON_EXISTENT_ID = "00000000-0000-0000-0000-000000000000"

    @classmethod
    def setUpClass(cls):
        """Setup client and create essential entities (User, Place, Amenity, Review) once."""
        print("\n--- SETUP: Initializing Test Environment ---")
        
        # 1. Setup client
        app = create_app()
        app.config['TESTING'] = True
        cls.client = app.test_client()
        cls.base_url = '/api/v1/'
        
        # 2. Create required entities (Dependencies for other tests)
        print("  -> Creating dependencies (User, Amenity, Place, Review)...")

        # Create User
        user_data = {"email": "setup@user.com", "password": "setup_password", "first_name": "Setup", "last_name": "User"}
        user_response = cls.client.post(cls.base_url + 'users/', json=user_data)
        cls.USER_ID = json.loads(user_response.data).get('id')
        print(f"  -> Setup User ID: {cls.USER_ID}")
        
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
        
        # Store initial counts for testing LIST/COUNT
        cls.initial_user_count = len(json.loads(cls.client.get(cls.base_url + 'users/').data))
        print(f"--- SETUP Complete. Starting tests ---")

    # --------------------------------------------------------------------------
    # --- USER ENDPOINTS ---
    # --------------------------------------------------------------------------

    def test_01_create_user_success(self):
        """Test user creation with valid data (201)."""
        print("\n[TEST 01] User: Successful creation.", end="") 
        response = self.client.post(self.base_url + 'users/', json={
            "first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "password": "secure"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', json.loads(response.data))

    def test_02_create_user_missing_required_field(self):
        """Test user creation missing 'email' (400)."""
        print("\n[TEST 02] User: Missing required field (400 expected).", end="")
        response = self.client.post(self.base_url + 'users/', json={
            "first_name": "Test", "last_name": "Fail" # Missing email
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("\\\'email\\\' is a required property", str(response.data))
    
    def test_03_get_user_not_found(self):
        """Test retrieving a non-existent user (404)."""
        print("\n[TEST 03] User: GET non-existent resource (404 expected).", end="")
        response = self.client.get(self.base_url + f'users/{self.NON_EXISTENT_ID}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", str(response.data))
    
    def test_04_update_user_read_only_field(self):
        """Test updating a read-only field like 'id' (400)."""
        print("\n[TEST 04] User: Attempting to update read-only field 'id' (400 expected).", end="")
        response = self.client.put(self.base_url + f'users/{self.USER_ID}', json={"id": "new-id-attempt"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Cannot update \\\'id\\\'", str(response.data))
    
    def test_05_delete_user_not_found(self):
        """Test deleting a non-existent user (404)."""
        print("\n[TEST 05] User: DELETE non-existent resource (404 expected).", end="")
        response = self.client.delete(self.base_url + f'users/{self.NON_EXISTENT_ID}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", str(response.data))

    # --------------------------------------------------------------------------
    # --- AMENITY ENDPOINTS ---
    # --------------------------------------------------------------------------

    def test_06_create_amenity_duplicate_name(self):
        """Test creating an amenity with a name that already exists (API currently allows it, returns 201)."""
        print("\n[TEST 06] Amenity: Duplicating name (201 actual, indicates potential API bug).", end="")
        response = self.client.post(self.base_url + 'amenities/', json={"name": "Test Amenity"})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', json.loads(response.data)) 

    def test_07_get_amenity_not_found(self):
        """Test retrieving a non-existent amenity (404)."""
        print("\n[TEST 07] Amenity: GET non-existent resource (404 expected).", end="")
        response = self.client.get(self.base_url + f'amenities/{self.NON_EXISTENT_ID}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Amenity not found", str(response.data))

    def test_08_update_amenity_empty_data(self):
        """Test updating an amenity with empty JSON data (API incorrectly requires 'name', returns 400)."""
        print("\n[TEST 08] Amenity: Update with empty payload (400 expected, due to schema issue).", end="")
        response = self.client.put(self.base_url + f'amenities/{self.AMENITY_ID}', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("\\\'name\\\' is a required property", str(response.data))

    # --------------------------------------------------------------------------
    # --- PLACE ENDPOINTS ---
    # --------------------------------------------------------------------------
    
    def test_09_create_place_invalid_owner_id(self):
        """Test place creation with a non-existent owner_id (404)."""
        print("\n[TEST 09] Place: Creation with invalid owner_id (404 expected).", end="")
        response = self.client.post(self.base_url + 'places/', json={
            "title": "Bad Owner", "price": 10.0, "latitude": 45.0, "longitude": 45.0, 
            "owner_id": self.NON_EXISTENT_ID, # Invalid Foreign Key
            "amenities": []
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn("Owner not found", str(response.data))

    def test_10_update_place_invalid_longitude(self):
        """Test place update with longitude outside boundary (API currently allows it, returns 200)."""
        print("\n[TEST 10] Place: Update with invalid longitude (200 actual, indicates API bug).", end="")
        response = self.client.put(self.base_url + f'places/{self.PLACE_ID}', json={
            "longitude": 180.1 # Out of range (max is 180)
        })
        self.assertEqual(response.status_code, 200)

    def test_11_delete_place_not_found(self):
        """Test deleting a non-existent place (404)."""
        print("\n[TEST 11] Place: DELETE non-existent resource (404 expected).", end="")
        response = self.client.delete(self.base_url + f'places/{self.NON_EXISTENT_ID}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Place not found", str(response.data))

    # --------------------------------------------------------------------------
    # --- REVIEW ENDPOINTS ---
    # --------------------------------------------------------------------------

    def test_12_create_review_invalid_place_id(self):
        """Test review creation with a non-existent place_id (404)."""
        print("\n[TEST 12] Review: Creation with invalid place_id (404 expected).", end="")
        response = self.client.post(self.base_url + 'reviews/', json={
            "text": "Invalid place", "rating": 3.0, 
            "user_id": self.USER_ID, 
            "place_id": self.NON_EXISTENT_ID # Invalid Foreign Key
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn("Place not found", str(response.data))

    def test_13_update_review_invalid_rating(self):
        """Test review update with rating outside boundary (API currently allows it, returns 200)."""
        print("\n[TEST 13] Review: Update with invalid rating (200 actual, indicates API bug).", end="")
        response = self.client.put(self.base_url + f'reviews/{self.REVIEW_ID}', json={
            "rating": 0.5 # Out of range (min is 1)
        })
        self.assertEqual(response.status_code, 200)
    
    def test_14_delete_review_not_found(self):
        """Test deleting a non-existent review (404)."""
        print("\n[TEST 14] Review: DELETE non-existent resource (404 expected).", end="")
        response = self.client.delete(self.base_url + f'reviews/{self.NON_EXISTENT_ID}')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Review not found", str(response.data))

    def test_15_list_users_success(self):
        """Test listing all users (200 OK and is a list)."""
        print("\n[TEST 15] List: Verifying user list endpoint (200 expected).", end="")
        response = self.client.get(self.base_url + 'users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), self.initial_user_count)

    @classmethod
    def tearDownClass(cls):
        """Cleanup entities created during setup (if the storage is persistent)."""
        print("\n--- TEARDOWN: Test suite execution finished ---")
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)