import hashlib
import urllib.parse
import requests
from typing import Dict
import os

class PaymentProcessor:
    def __init__(self):
        self.merchant_id = os.getenv('PAYFAST_MERCHANT_ID', '10000100')
        self.merchant_key = os.getenv('PAYFAST_MERCHANT_KEY', '46f0cd694581a')
        self.return_url = os.getenv('PAYFAST_RETURN_URL', 'http://localhost:3000/payment/success')
        self.cancel_url = os.getenv('PAYFAST_CANCEL_URL', 'http://localhost:3000/payment/cancel')
        self.notify_url = os.getenv('PAYFAST_NOTIFY_URL', 'http://localhost:5000/api/payments/notify')
        self.payfast_url = os.getenv('PAYFAST_URL', 'https://sandbox.payfast.co.za/eng/process')
        
    def generate_payfast_payment(self, amount: float, user_id: str, payment_id: str, user_data: Dict) -> Dict:
        """Generate PayFast payment data"""
        
        amount = float(amount)
        data = {
            'merchant_id': self.merchant_id,
            'merchant_key': self.merchant_key,
            'return_url': self.return_url,
            'cancel_url': self.cancel_url,
            'notify_url': self.notify_url,
            'name_first': user_data.get('first_name', ''),
            'name_last': user_data.get('last_name', ''),
            'email_address': user_data.get('email', ''),
            'm_payment_id': payment_id,
            'amount': f"{amount:.2f}",
            'item_name': f"Job Application Service - R{amount:.0f}",
            'item_description': 'Automated job application service for South Africa',
            'custom_int1': user_id,
        }
        
        # Generate signature
        signature_string = "&".join([f"{key}={urllib.parse.quote_plus(str(value))}" for key, value in data.items()])
        data['signature'] = hashlib.md5(signature_string.encode()).hexdigest()
        
        return {
            'payment_url': self.payfast_url,
            'payment_data': data
        }
    
    def verify_payfast_payment(self, data: Dict) -> bool:
        """Verify PayFast payment notification"""
        try:
            # Extract signature from data
            received_signature = data.get('signature')
            if not received_signature:
                return False
            
            # Create our own signature
            temp_data = data.copy()
            temp_data.pop('signature', None)
            
            signature_string = "&".join([f"{key}={urllib.parse.quote_plus(str(value))}" for key, value in temp_data.items()])
            calculated_signature = hashlib.md5(signature_string.encode()).hexdigest()
            
            return received_signature == calculated_signature
            
        except Exception as e:
            print(f"Payment verification error: {e}")
            return False
    
    def generate_eft_payment(self, amount: float, user_id: str, payment_id: str) -> Dict:
        """Generate EFT payment details"""
        
        bank_details = {
            'bank_name': 'Standard Bank',
            'account_name': 'JobApp Automator (Pty) Ltd',
            'account_number': '000334789123',  # Replace with actual account
            'account_type': 'Business Current Account',
            'branch_code': '000334',
            'branch_name': 'Sandton City',
            'reference': f"JOBAPP{payment_id[:8].upper()}",
            'amount': f"R{amount:.2f}",
            'beneficiary': 'JobApp Automator (Pty) Ltd',
            'swift_code': 'SBZAZAJJ',
            'instructions': [
                'Use the exact reference number when making payment',
                'Email proof of payment to payments@jobappautomator.co.za',
                'Access will be granted within 24 hours of payment confirmation'
            ]
        }
        
        return bank_details
    
    def check_eft_payment_status(self, payment_reference: str) -> Dict:
        """Check EFT payment status (mock implementation)"""
        # In a real implementation, this would integrate with your bank's API
        # or payment verification system
        
        return {
            'status': 'pending',  # pending, verified, failed
            'reference': payment_reference,
            'checked_at': '2024-01-01T00:00:00Z',
            'message': 'Payment verification in progress'
        }
