import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { agentAPI, ticketAPI } from '../../services/api';
import { FiRefreshCw, FiFilter, FiSearch } from 'react-icons/fi';
import LoadingSpinner from '../Common/LoadingSpinner';

const AgentQueue = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchQueue();
  }, [filter]);

  const fetchQueue = async () => {
    setLoading(true);
    try {
      const response = await ticketAPI.getAll();
      let filteredTickets = response.data;
      
      if (filter !== 'all') {
        filteredTickets = filteredTickets.filter(t => t.status === filter);
      }
      
      // Sort by priority (P1 highest)
      const priorityOrder = { P1: 1, P2: 2, P3: 3, P4: 4 };
      filteredTickets.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
      
      setTickets(filteredTickets);
    } catch (error) {
      console.error('Failed to fetch queue:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredTickets = tickets.filter(ticket =>
    ticket.title.toLowerCase().includes(search.toLowerCase()) ||
    ticket.description.toLowerCase().includes(search.toLowerCase()) ||
    `#${ticket.ticket_id}`.includes(search)
  );

  const priorityColors = {
    P1: 'bg-red-100 text-red-800 border-red-200',
    P2: 'bg-orange-100 text-orange-800 border-orange-200',
    P3: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    P4: 'bg-green-100 text-green-800 border-green-200'
  };

  const statusBadges = {
    open: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    resolved: 'bg-green-100 text-green-800',
    closed: 'bg-gray-100 text-gray-800'
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Support Queue</h1>
          <p className="text-gray-600 mt-1">Manage and prioritize customer support tickets</p>
        </div>
        <button onClick={fetchQueue} className="btn-secondary flex items-center space-x-2">
          <FiRefreshCw className="h-4 w-4" />
          <span>Refresh</span>
        </button>
      </div>

      {/* Filters */}
      <div className="mb-6 flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search tickets..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field pl-10"
          />
        </div>
        <div className="flex items-center space-x-2">
          <FiFilter className="text-gray-400" />
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="input-field w-auto"
          >
            <option value="all">All Tickets</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
        </div>
      </div>

      {/* Queue Grid */}
      {filteredTickets.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No tickets in queue</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {filteredTickets.map((ticket) => (
            <div key={ticket.ticket_id} className={`card border-l-4 ${priorityColors[ticket.priority]}`}>
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-sm font-mono text-gray-500">#{ticket.ticket_id}</span>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusBadges[ticket.status]}`}>
                      {ticket.status.replace('_', ' ')}
                    </span>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${priorityColors[ticket.priority]}`}>
                      {ticket.priority}
                    </span>
                  </div>
                  <Link to={`/tickets/${ticket.ticket_id}`}>
                    <h3 className="text-lg font-semibold text-gray-900 hover:text-primary-600 mb-2">
                      {ticket.title}
                    </h3>
                  </Link>
                  <p className="text-gray-600 line-clamp-2 mb-3">{ticket.description}</p>
                  <div className="flex items-center text-sm text-gray-500 space-x-4">
                    <span>From: {ticket.user?.name || 'Anonymous'}</span>
                    <span>Created: {new Date(ticket.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <Link
                  to={`/tickets/${ticket.ticket_id}`}
                  className="btn-primary text-sm py-1 px-3"
                >
                  View & Respond
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AgentQueue;