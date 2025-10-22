import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState({
        totalApplications: 0,
        jobsFound: 0,
        activeSearches: 0
    });

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const token = localStorage.getItem('token');
            const [userResponse, appsResponse] = await Promise.all([
                axios.get('/api/auth/profile', {
                    headers: { Authorization: `Bearer ${token}` }
                }),
                axios.get('/api/applications/history', {
                    headers: { Authorization: `Bearer ${token}` }
                })
            ]);

            setUser(userResponse.data.user);
            setApplications(appsResponse.data.applications || []);

            // Calculate stats
            const totalApps = appsResponse.data.applications?.length || 0;
            const jobsFound = appsResponse.data.applications?.reduce((acc, app) => acc + (app.matches_found || 0), 0) || 0;
            const activeSearches = appsResponse.data.applications?.filter(app => app.status === 'processing').length || 0;

            setStats({
                totalApplications: totalApps,
                jobsFound: jobsFound,
                activeSearches: activeSearches
            });
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="container mx-auto px-4">
                {/* Welcome Section */}
                <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
                    <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                        <div>
                            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
                                Welcome back, {user?.first_name}!
                            </h1>
                            <p className="text-gray-600 mt-2">
                                Ready to continue your job search across South Africa?
                            </p>
                        </div>
                        <Link 
                            to="/new-application"
                            className="mt-4 md:mt-0 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                        >
                            Start New Job Search
                        </Link>
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-white rounded-xl shadow-sm p-6">
                        <div className="flex items-center">
                            <div className="bg-blue-100 p-3 rounded-lg mr-4">
                                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Total Applications</p>
                                <p className="text-2xl font-bold text-gray-800">{stats.totalApplications}</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-xl shadow-sm p-6">
                        <div className="flex items-center">
                            <div className="bg-green-100 p-3 rounded-lg mr-4">
                                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
                                </svg>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Jobs Found</p>
                                <p className="text-2xl font-bold text-gray-800">{stats.jobsFound}</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-xl shadow-sm p-6">
                        <div className="flex items-center">
                            <div className="bg-orange-100 p-3 rounded-lg mr-4">
                                <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </div>
                            <div>
                                <p className="text-sm text-gray-600">Active Searches</p>
                                <p className="text-2xl font-bold text-gray-800">{stats.activeSearches}</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Recent Applications */}
                <div className="bg-white rounded-xl shadow-sm p-6">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl font-bold text-gray-800">Recent Job Searches</h2>
                        <Link 
                            to="/applications"
                            className="text-blue-600 hover:text-blue-700 font-medium"
                        >
                            View All
                        </Link>
                    </div>

                    {applications.length === 0 ? (
                        <div className="text-center py-12">
                            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">No job searches yet</h3>
                            <p className="text-gray-500 mb-4">Start your first automated job search to find opportunities across South Africa.</p>
                            <Link 
                                to="/new-application"
                                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                            >
                                Start Your First Search
                            </Link>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {applications.slice(0, 5).map((application) => (
                                <div key={application.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
                                    <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                                        <div>
                                            <h3 className="font-semibold text-gray-800">
                                                {application.job_title || 'General Job Search'}
                                            </h3>
                                            <p className="text-gray-600 text-sm mt-1">
                                                {application.target_region} 
                                                {application.target_town && ` • ${application.target_town}`}
                                            </p>
                                        </div>
                                        <div className="flex items-center space-x-4 mt-2 md:mt-0">
                                            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                                                application.status === 'completed' 
                                                    ? 'bg-green-100 text-green-800'
                                                    : application.status === 'processing'
                                                    ? 'bg-blue-100 text-blue-800'
                                                    : 'bg-yellow-100 text-yellow-800'
                                            }`}>
                                                {application.status}
                                            </span>
                                            <span className="text-sm text-gray-600">
                                                {application.matches_found} jobs found
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Quick Actions */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                    <div className="bg-white rounded-xl shadow-sm p-6">
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">Need Help?</h3>
                        <p className="text-gray-600 mb-4">
                            Check out our comprehensive guide on how to make the most of your job search.
                        </p>
                        <Link 
                            to="/help"
                            className="text-blue-600 hover:text-blue-700 font-medium"
                        >
                            Visit Help Center →
                        </Link>
                    </div>

                    <div className="bg-white rounded-xl shadow-sm p-6">
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">Update Your Profile</h3>
                        <p className="text-gray-600 mb-4">
                            Keep your information up to date for better job matching.
                        </p>
                        <Link 
                            to="/profile"
                            className="text-blue-600 hover:text-blue-700 font-medium"
                        >
                            Edit Profile →
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
