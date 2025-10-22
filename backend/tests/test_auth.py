import unittest
import json
from app import create_app, db
from app.models.user import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post('/api/auth/register', 
            json={
                'email': 'test@example.com',
                'password': 'TestPassword123!',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '0123456789'
            }
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('user', data)

    def test_user_registration_invalid_email(self):
        """Test user registration with invalid email"""
        response = self.client.post('/api/auth/register', 
            json={
                'email': 'invalid-email',
                'password': 'TestPassword123!',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        """Test user login"""
        # First register a user
        self.client.post('/api/auth/register', 
            json={
                'email': 'test@example.com',
                'password': 'TestPassword123!',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        
        # Then login
        response = self.client.post('/api/auth/login', 
            json={
                'email': 'test@example.com',
                'password': 'TestPassword123!'
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)

    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials"""
        response = self.client.post('/api/auth/login', 
            json={
                'email': 'nonexistent@example.com',
                'password': 'wrongpassword'
            }
        )
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
