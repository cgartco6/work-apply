import React, { useState } from 'react';
import axios from 'axios';

const PaymentForm = ({ onPaymentSuccess }) => {
    const [paymentMethod, setPaymentMethod] = useState('payfast');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const initiatePayment = async () => {
        setLoading(true);
        setError('');
        
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post('/api/payments/initiate', {
                payment_method: paymentMethod
            }, {
                headers: { 
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
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
            setError('Payment initiation failed. Please try again.');
        }
        setLoading(false);
    };

    return (
        <div className="max-w-md mx-auto bg-white rounded-xl shadow-lg overflow-hidden p-6">
            <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">Complete Your Payment</h2>
                <p className="text-gray-600 mt-2">One-time payment of R499 for full access</p>
            </div>

            {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
                    {error}
                </div>
            )}

            <div className="mb-6">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                    <div className="flex justify-between items-center">
                        <span className="font-semibold text-gray-700">Service Fee</span>
                        <span className="text-2xl font-bold text-blue-600">R499.00</span>
                    </div>
                    <p className="text-sm text-gray-600 mt-2">
                        Includes AI resume enhancement, cover letter generation, and automated job applications across South Africa
                    </p>
                </div>
            </div>

            <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                    Select Payment Method
                </label>
                <div className="space-y-3">
                    <label className="flex items-center p-3 border border-gray-300 rounded-lg hover:border-blue-500 cursor-pointer">
                        <input
                            type="radio"
                            value="payfast"
                            checked={paymentMethod === 'payfast'}
                            onChange={(e) => setPaymentMethod(e.target.value)}
                            className="mr-3 text-blue-600 focus:ring-blue-500"
                        />
                        <div>
                            <span className="font-medium">PayFast</span>
                            <p className="text-sm text-gray-600">Credit Card, Debit Card, Instant EFT</p>
                        </div>
                    </label>
                    
                    <label className="flex items-center p-3 border border-gray-300 rounded-lg hover:border-blue-500 cursor-pointer">
                        <input
                            type="radio"
                            value="eft"
                            checked={paymentMethod === 'eft'}
                            onChange={(e) => setPaymentMethod(e.target.value)}
                            className="mr-3 text-blue-600 focus:ring-blue-500"
                        />
                        <div>
                            <span className="font-medium">Direct EFT/Bank Transfer</span>
                            <p className="text-sm text-gray-600">Bank transfer with manual verification</p>
                        </div>
                    </label>
                </div>
            </div>

            <button
                onClick={initiatePayment}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-semibold"
            >
                {loading ? (
                    <div className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Processing...
                    </div>
                ) : (
                    `Pay R499.00 with ${paymentMethod === 'payfast' ? 'PayFast' : 'EFT'}`
                )}
            </button>

            <div className="mt-4 text-center">
                <p className="text-xs text-gray-500">
                    Secure payment processed by PayFast. Your financial information is encrypted and secure.
                </p>
            </div>
        </div>
    );
};

export default PaymentForm;
