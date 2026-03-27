import React from 'react';
import { Link } from 'react-router-dom';
import { FiClock, FiTag, FiUser } from 'react-icons/fi';

const TicketCard = ({ ticket }) => {
  const statusColors = {
    open: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    resolved: 'bg-green-100 text-green-800',
    closed: 'bg-gray-100 text-gray-800'
  };

  const priorityColors = {
    P1: 'bg-red-100 text-red-800',
    P2: 'bg-orange-100 text-orange-800',
    P3: 'bg-yellow-100 text-yellow-800',
    P4: 'bg-green-100 text-green-800'
  };

  return (
    <Link to={`/tickets/${ticket.ticket_id}`} className="block">
      <div className="card hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start mb-3">
          <h3 className="text-lg font-semibold text-gray-900">{ticket.title}</h3>
          <div className="flex space-x-2">
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColors[ticket.status]}`}>
              {ticket.status.replace('_', ' ')}
            </span>
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${priorityColors[ticket.priority]}`}>
              {ticket.priority}
            </span>
          </div>
        </div>
        <p className="text-gray-600 mb-4 line-clamp-2">{ticket.description}</p>
        <div className="flex items-center text-sm text-gray-500 space-x-4">
          <div className="flex items-center space-x-1">
            <FiClock className="h-4 w-4" />
            <span>{new Date(ticket.created_at).toLocaleDateString()}</span>
          </div>
          <div className="flex items-center space-x-1">
            <FiTag className="h-4 w-4" />
            <span>ID: #{ticket.ticket_id}</span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default TicketCard;