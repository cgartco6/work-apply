from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.payment import Payment
from app.models.user import User
from app import db
from app.services.payment_processor import PaymentProcessor

payments_bp = Blueprint('payments', __name__)
payment_processor = PaymentProcessor()

@payments_bp.route('/initiate', methods=['POST'])
@jwt_required()
def initiate_payment():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    payment_method = data.get('payment_method')
    
    if payment_method not in ['payfast', 'eft']:
        return jsonify({'error': 'Invalid payment method'}), 400
    
    # Create payment record
    payment = Payment(
        user_id=user_id,
        amount=499.00,
        payment_method=payment_method,
        status='pending'
    )
    
    db.session.add(payment)
    db.session.commit()
    
    if payment_method == 'payfast':
        payment_data = payment_processor.generate_payfast_payment(
            amount=499.00,
            user_id=user_id,
            payment_id=payment.id
        )
        
        return jsonify({
            'payment_id': payment.id,
            'payment_url': payment_data['payment_url'],
            'payment_data': payment_data['payment_data']
        })
    
    elif payment_method == 'eft':
        eft_details = payment_processor.generate_eft_payment(
            amount=499.00,
            user_id=user_id,
            payment_id=payment.id
        )
        
        payment.eft_reference = eft_details['reference']
        db.session.commit()
        
        return jsonify({
            'payment_id': payment.id,
            'eft_details': eft_details
        })

@payments_bp.route('/notify', methods=['POST'])
def payment_notify():
    """PayFast ITN (Instant Transaction Notification) endpoint"""
    data = request.form.to_dict()
    
    if not payment_processor.verify_payfast_payment(data):
        return jsonify({'status': 'error'}), 400
    
    payment_id = data.get('m_payment_id')
    payment_status = data.get('payment_status')
    
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'status': 'error'}), 404
    
    if payment_status == 'COMPLETE':
        payment.status = 'completed'
        # Activate user access
        user = User.query.get(payment.user_id)
        if user:
            user.is_verified = True
    else:
        payment.status = 'failed'
    
    db.session.commit()
    
    return jsonify({'status': 'ok'})

@payments_bp.route('/status/<payment_id>', methods=['GET'])
@jwt_required()
def payment_status(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    return jsonify(payment.to_dict())
