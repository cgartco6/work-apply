import React, { useState } from 'react';
import axios from 'axios';

const PaymentForm = ({ onPaymentSuccess }) => {
    const [paymentMethod, setPaymentMethod] = useState('payfast');
    const [loading, setLoading] = useState(false);

    const initiatePayment = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post('/api/payments/initiate', {
                payment_method: paymentMethod
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (paymentMethod === 'payfast') {
                // Submit form to PayFast
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = response.data.payment_url;
                
                Object.entries(response.data.payment_data).forEach(([key, value]) => {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = key;
                    input.value = value;
                    form.appendChild(input);
                });
                
                document.body.appendChild(form);
                form.submit();
            } else {
                // Show EFT details
                onPaymentSuccess(response.data);
            }
        } catch (error) {
            console.error('Payment initiation failed:', error);
            alert('Payment initiation failed. Please try again.');
        }
        setLoading(false);
    };

    return (
        <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Payment Required</h2>
            
            <div className="mb-6">
                <p className="text-lg font-semibold text-gray-700">Service Fee: R499.00</p>
                <p className="text-sm text-gray-600 mt-2">
                    Access our AI-powered job application service for South Africa
                </p>
            </div>

            <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                    Select Payment Method
                </label>
                <div className="space-y-2">
                    <label className="flex items-center">
                        <input
                            type="radio"
                            value="payfast"
                            checked={paymentMethod === 'payfast'}
                            onChange={(e) => setPaymentMethod(e.target.value)}
                            className="mr-2"
                        />
                        <span>PayFast (Credit Card, Instant EFT)</span>
                    </label>
                    <label className="flex items-center">
                        <input
                            type="radio"
                            value="eft"
                            checked={paymentMethod === 'eft'}
                            onChange={(e) => setPaymentMethod(e.target.value)}
                            className="mr-2"
                        />
                        <span>Direct EFT/Bank Transfer</span>
                    </label>
                </div>
            </div>

            <button
                onClick={initiatePayment}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
            >
                {loading ? 'Processing...' : `Pay R499.00 with ${paymentMethod === 'payfast' ? 'PayFast' : 'EFT'}`}
            </button>
        </div>
    );
};

export default PaymentForm;
