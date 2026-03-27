import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ticketAPI, agentAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { FiUsers, FiClock, FiCheckCircle, FiAlertCircle, FiBarChart2, FiTrendingUp } from 'react-icons/fi';
import LoadingSpinner from '../Common/LoadingSpinner';

const AgentDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    total: 0,
    open: 0,
    inProgress: 0,
    resolved: 0,
    avgResponseTime: 0
  });
  const [recentTickets, setRecentTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAgentData();
  }, []);

  const fetchAgentData = async () => {
    try {
      const response = await ticketAPI.getAll();
      const tickets = response.data;
      
      // Calculate stats
      const openTickets = tickets.filter(t => t.status === 'open');
      const inProgressTickets = tickets.filter(t => t.status === 'in_progress');
      const resolvedTickets = tickets.filter(t => t.status === 'resolved');
      
      // Calculate average response time (mock data for now)
      const avgResponse = 45; // minutes
      
      setStats({
        total: tickets.length,
        open: openTickets.length,
        inProgress: inProgressTickets.length,
        resolved: resolvedTickets.length,
        avgResponseTime: avgResponse
      });
      
      // Get priority sorted tickets
      const priorityOrder = { P1: 1, P2: 2, P3: 3, P4: 4 };
      const sortedTickets = [...tickets].sort((a, b) => 
        priorityOrder[a.priority] - priorityOrder[b.priority]
      );
      setRecentTickets(sortedTickets.slice(0, 10));
      
    } catch (error) {
      console.error('Failed to fetch agent data:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateTicketStatus = async (ticketId, status) => {
    try {
      await ticketAPI.update(ticketId, { status });
      await fetchAgentData();
    } catch (error) {
      console.error('Failed to update ticket:', error);
    }
  };

  const statCards = [
    { label: 'Total Tickets', value: stats.total, icon: FiBarChart2, color: 'bg-blue-500', change: '+12%' },
    { label: 'Open Tickets', value: stats.open, icon: FiAlertCircle, color: 'bg-yellow-500', change: '+5%' },
    { label: 'In Progress', value: stats.inProgress, icon: FiClock, color: 'bg-orange-500', change: '-3%' },
    { label: 'Resolved', value: stats.resolved, icon: FiCheckCircle, color: 'bg-green-500', change: '+8%' },
    { label: 'Avg Response', value: `${stats.avgResponseTime}m`, icon: FiTrendingUp, color: 'bg-purple-500', change: '-2m' }
  ];

  const priorityColors = {
    P1: 'bg-red-100 text-red-800',
    P2: 'bg-orange-100 text-orange-800',
    P3: 'bg-yellow-100 text-yellow-800',
    P4: 'bg-green-100 text-green-800'
  };

  const statusColors = {
    open: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    resolved: 'bg-green-100 text-green-800',
    closed: 'bg-gray-100 text-gray-800'
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Agent Dashboard</h1>
        <p className="text-gray-600">Welcome back, {user?.name}! Manage and resolve customer tickets efficiently.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
        {statCards.map((card, index) => {
          const Icon = card.icon;
          return (
            <div key={index} className="card">
              <div className="flex items-center justify-between mb-2">
                <div className={`${card.color} p-2 rounded-lg`}>
                  <Icon className="h-5 w-5 text-white" />
                </div>
                <span className={`text-xs font-medium ${
                  card.change.startsWith('+') ? 'text-green-600' : 'text-red-600'
                }`}>
                  {card.change}
                </span>
              </div>
              <p className="text-2xl font-bold text-gray-900">{card.value}</p>
              <p className="text-sm text-gray-600">{card.label}</p>
            </div>
          );
        })}
      </div>

      {/* Tickets Table */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Support Queue</h2>
          <div className="flex space-x-2">
            <button className="btn-secondary text-sm px-3 py-1">All Tickets</button>
            <button className="text-sm px-3 py-1 text-gray-600 hover:bg-gray-100 rounded">Open</button>
            <button className="text-sm px-3 py-1 text-gray-600 hover:bg-gray-100 rounded">In Progress</button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {recentTickets.map((ticket) => (
                <tr key={ticket.ticket_id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-900">#{ticket.ticket_id}</td>
                  <td className="px-4 py-3">
                    <Link to={`/tickets/${ticket.ticket_id}`} className="text-sm text-primary-600 hover:text-primary-800">
                      {ticket.title}
                    </Link>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${priorityColors[ticket.priority]}`}>
                      {ticket.priority}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColors[ticket.status]}`}>
                      {ticket.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {new Date(ticket.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3">
                    <select
                      value={ticket.status}
                      onChange={(e) => updateTicketStatus(ticket.ticket_id, e.target.value)}
                      className="text-sm border rounded px-2 py-1"
                    >
                      <option value="open">Open</option>
                      <option value="in_progress">In Progress</option>
                      <option value="resolved">Resolved</option>
                      <option value="closed">Closed</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AgentDashboard;