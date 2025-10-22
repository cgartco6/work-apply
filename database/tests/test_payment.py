import unittest
import json
from app import create_app, db
from app.models.user import User, Payment

class PaymentsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        # Create a test user
        self.user_data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        response = self.client.post('/api/auth/register', json=self.user_data)
        self.auth_token = json.loads(response.data)['access_token']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_initiate_payment(self):
        """Test payment initiation"""
        response = self.client.post('/api/payments/initiate', 
            json={'payment_method': 'eft'},
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('payment_id', data)
        self.assertIn('eft_details', data)

    def test_payment_status(self):
        """Test payment status check"""
        # First create a payment
        payment_response = self.client.post('/api/payments/initiate', 
            json={'payment_method': 'eft'},
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        payment_id = json.loads(payment_response.data)['payment_id']
        
        # Check status
        response = self.client.get(f'/api/payments/status/{payment_id}',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'pending')

if __name__ == '__main__':
    unittest.main()
