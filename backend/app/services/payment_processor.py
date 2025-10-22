import hashlib
import urllib.parse
import requests
from typing import Dict

class PaymentProcessor:
    def __init__(self):
        self.merchant_id = "10000100"  # PayFast test merchant ID
        self.merchant_key = "46f0cd694581a"  # PayFast test merchant key
        self.return_url = "https://yourdomain.com/payment/success"
        self.cancel_url = "https://yourdomain.com/payment/cancel"
        self.notify_url = "https://yourdomain.com/api/payments/notify"
        
    def generate_payfast_payment(self, amount: float, user_id: str, payment_id: str) -> Dict:
        """Generate PayFast payment data"""
        
        amount = float(amount)
        data = {
            'merchant_id': self.merchant_id,
            'merchant_key': self.merchant_key,
            'return_url': self.return_url,
            'cancel_url': self.cancel_url,
            'notify_url': self.notify_url,
            'name_first': 'Client',
            'email_address': 'client@example.com',
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
            'payment_url': 'https://sandbox.payfast.co.za/eng/process',
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
            'account_number': '000000000',  # Replace with actual account
            'branch_code': '000000',
            'branch_name': 'Sandton',
            'reference': f"JOBAPP{payment_id[:8].upper()}",
            'amount': f"R{amount:.2f}",
            'beneficiary': 'JobApp Automator (Pty) Ltd'
        }
        
        return bank_details
