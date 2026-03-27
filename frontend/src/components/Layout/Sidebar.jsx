import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  FiHome, FiList, FiPlusCircle, FiMessageSquare, 
  FiHelpCircle, FiBarChart2, FiUsers 
} from 'react-icons/fi';
import { useAuth } from '../../context/AuthContext';

const Sidebar = () => {
  const location = useLocation();
  const { user } = useAuth();

  const menuItems = [
    { path: '/dashboard', icon: FiHome, label: 'Dashboard' },
    { path: '/tickets', icon: FiList, label: 'My Tickets' },
    { path: '/create-ticket', icon: FiPlusCircle, label: 'New Ticket' },
    { path: '/chat', icon: FiMessageSquare, label: 'AI Chat' },
    { path: '/faq', icon: FiHelpCircle, label: 'FAQ' },
  ];

  if (user?.is_admin) {
    menuItems.push({ path: '/agent-dashboard', icon: FiUsers, label: 'Agent Dashboard' });
    menuItems.push({ path: '/analytics', icon: FiBarChart2, label: 'Analytics' });
  }

  return (
    <aside className="w-64 bg-white shadow-lg h-full">
      <nav className="mt-5 px-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md mb-1 ${
                isActive
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`}
            >
              <Icon className={`mr-3 h-5 w-5 ${isActive ? 'text-primary-500' : 'text-gray-400'}`} />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
};

export default Sidebar;