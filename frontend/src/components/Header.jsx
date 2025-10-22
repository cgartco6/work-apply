import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Header = () => {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/');
    };

    return (
        <header className="bg-white shadow-sm border-b">
            <div className="container mx-auto px-4 py-4">
                <div className="flex justify-between items-center">
                    <Link to="/" className="flex items-center space-x-2">
                        <div className="w-8 h-8 bg-blue-600 rounded-lg"></div>
                        <span className="text-xl font-bold text-gray-800">JobApp Automator</span>
                    </Link>
                    
                    <nav className="hidden md:flex items-center space-x-8">
                        {token ? (
                            <>
                                <Link to="/dashboard" className="text-gray-600 hover:text-blue-600 font-medium">
                                    Dashboard
                                </Link>
                                <Link to="/applications" className="text-gray-600 hover:text-blue-600 font-medium">
                                    My Applications
                                </Link>
                                <Link to="/profile" className="text-gray-600 hover:text-blue-600 font-medium">
                                    Profile
                                </Link>
                                <button 
                                    onClick={handleLogout}
                                    className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
                                >
                                    Logout
                                </button>
                            </>
                        ) : (
                            <>
                                <Link to="/" className="text-gray-600 hover:text-blue-600 font-medium">
                                    Home
                                </Link>
                                <Link to="/pricing" className="text-gray-600 hover:text-blue-600 font-medium">
                                    Pricing
                                </Link>
                                <Link to="/login" className="text-gray-600 hover:text-blue-600 font-medium">
                                    Login
                                </Link>
                                <Link 
                                    to="/register" 
                                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                                >
                                    Get Started
                                </Link>
                            </>
                        )}
                    </nav>

                    {/* Mobile menu button */}
                    <button className="md:hidden text-gray-600">
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </header>
    );
};

export default Header;
