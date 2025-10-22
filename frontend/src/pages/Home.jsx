import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            {/* Hero Section */}
            <section className="py-20 px-4">
                <div className="container mx-auto text-center">
                    <h1 className="text-5xl md:text-6xl font-bold text-gray-800 mb-6">
                        Automate Your Job Search in 
                        <span className="text-blue-600"> South Africa</span>
                    </h1>
                    <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
                        Let our AI agents rewrite your resume, generate cover letters, and apply to hundreds of jobs across South Africa. All for one flat fee.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link 
                            to="/register" 
                            className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
                        >
                            Start Your Job Search - R499
                        </Link>
                        <Link 
                            to="/how-it-works" 
                            className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-50 transition-colors"
                        >
                            How It Works
                        </Link>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-16 bg-white">
                <div className="container mx-auto px-4">
                    <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-800 mb-4">
                        How JobApp Automator Works
                    </h2>
                    <p className="text-xl text-gray-600 text-center mb-12 max-w-2xl mx-auto">
                        Four simple steps to land your dream job in South Africa
                    </p>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        <div className="text-center p-6">
                            <div className="bg-blue-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-blue-600 text-2xl font-bold">1</span>
                            </div>
                            <h3 className="text-xl font-semibold mb-3">Upload & Pay</h3>
                            <p className="text-gray-600">
                                Upload your resume and make a one-time payment of R499 for full access to our platform.
                            </p>
                        </div>
                        
                        <div className="text-center p-6">
                            <div className="bg-blue-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-blue-600 text-2xl font-bold">2</span>
                            </div>
                            <h3 className="text-xl font-semibold mb-3">AI Enhancement</h3>
                            <p className="text-gray-600">
                                Our AI rewrites and optimizes your resume for South African employers and ATS systems.
                            </p>
                        </div>
                        
                        <div className="text-center p-6">
                            <div className="bg-blue-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-blue-600 text-2xl font-bold">3</span>
                            </div>
                            <h3 className="text-xl font-semibold mb-3">Nationwide Search</h3>
                            <p className="text-gray-600">
                                We scan job portals across all 9 provinces and major towns in South Africa.
                            </p>
                        </div>
                        
                        <div className="text-center p-6">
                            <div className="bg-blue-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-blue-600 text-2xl font-bold">4</span>
                            </div>
                            <h3 className="text-xl font-semibold mb-3">Automated Applications</h3>
                            <p className="text-gray-600">
                                We handle the entire application process with personalized cover letters for each job.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Regions Covered */}
            <section className="py-16 bg-gray-50">
                <div className="container mx-auto px-4">
                    <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-800 mb-4">
                        We Cover All of South Africa
                    </h2>
                    <p className="text-xl text-gray-600 text-center mb-12 max-w-2xl mx-auto">
                        From Cape Town to Johannesburg, and everywhere in between
                    </p>
                    
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 max-w-4xl mx-auto">
                        {['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape', 'Free State', 
                          'Limpopo', 'Mpumalanga', 'North West', 'Northern Cape'].map((province) => (
                            <div key={province} className="bg-white p-4 rounded-lg shadow-sm text-center">
                                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                                    <span className="text-blue-600 font-semibold">✓</span>
                                </div>
                                <span className="font-medium text-gray-800">{province}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-16 bg-blue-600">
                <div className="container mx-auto px-4 text-center">
                    <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                        Ready to Transform Your Job Search?
                    </h2>
                    <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
                        Join thousands of South Africans who have found their dream jobs through our automated platform.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link 
                            to="/register" 
                            className="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg"
                        >
                            Get Started Now - R499
                        </Link>
                        <Link 
                            to="/login" 
                            className="border border-white text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                            Existing User? Login
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;
