import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { FiLogOut, FiUser, FiMessageSquare, FiHelpCircle, FiHome, FiList, FiPlusCircle } from 'react-icons/fi';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <FiMessageSquare className="h-8 w-8 text-primary-600" />
              <span className="font-bold text-xl text-gray-800">Support Agent</span>
            </Link>
          </div>

          {isAuthenticated && (
            <div className="flex items-center space-x-4">
              <Link to="/dashboard" className="text-gray-700 hover:text-primary-600">
                <FiHome className="h-5 w-5" />
              </Link>
              <Link to="/tickets" className="text-gray-700 hover:text-primary-600">
                <FiList className="h-5 w-5" />
              </Link>
              <Link to="/create-ticket" className="text-gray-700 hover:text-primary-600">
                <FiPlusCircle className="h-5 w-5" />
              </Link>
              <Link to="/faq" className="text-gray-700 hover:text-primary-600">
                <FiHelpCircle className="h-5 w-5" />
              </Link>
              {user?.is_admin && (
                <Link to="/agent-dashboard" className="text-gray-700 hover:text-primary-600">
                  Agent Dashboard
                </Link>
              )}
              <div className="flex items-center space-x-2">
                <FiUser className="h-5 w-5 text-gray-600" />
                <span className="text-sm text-gray-700">{user?.name}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-1 text-gray-700 hover:text-red-600"
              >
                <FiLogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;