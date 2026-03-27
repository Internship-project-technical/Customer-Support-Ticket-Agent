import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ticketAPI, agentAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import LoadingSpinner from '../Common/LoadingSpinner';
import { 
  FiArrowLeft, FiSend, FiUser, FiClock, FiTag, FiFlag, 
  FiMessageSquare, FiCpu, FiCoffee as FiBot
} from 'react-icons/fi';
import toast from 'react-hot-toast';

const TicketDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [ticket, setTicket] = useState(null);
  const [replies, setReplies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newMessage, setNewMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState(null);
  const [showAISuggestion, setShowAISuggestion] = useState(false);

  useEffect(() => {
    fetchTicket();
    fetchReplies();
    fetchAISuggestion();
  }, [id]);

  const fetchTicket = async () => {
    try {
      const response = await ticketAPI.getOne(id);
      setTicket(response.data);
    } catch (error) {
      toast.error('Failed to load ticket');
      navigate('/tickets');
    }
  };

  const fetchReplies = async () => {
    try {
      const response = await ticketAPI.getReplies(id);
      setReplies(response.data);
    } catch (error) {
      console.error('Failed to fetch replies:', error);
    }
  };

  const fetchAISuggestion = async () => {
    try {
      const response = await agentAPI.suggestReply(id);
      setAiSuggestion(response.data);
    } catch (error) {
      console.error('Failed to get AI suggestion:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendReply = async () => {
    if (!newMessage.trim()) return;
    setSending(true);
    try {
      await ticketAPI.addReply(id, newMessage, user?.is_admin ? 'agent' : 'user');
      setNewMessage('');
      await fetchReplies();
      toast.success('Reply sent!');
    } catch (error) {
      toast.error('Failed to send reply');
    } finally {
      setSending(false);
    }
  };

  const handleUseAISuggestion = () => {
    if (aiSuggestion) {
      setNewMessage(aiSuggestion.suggested_reply);
      setShowAISuggestion(false);
    }
  };

  const updateTicketStatus = async (status) => {
    try {
      await ticketAPI.update(id, { status });
      await fetchTicket();
      toast.success(`Ticket status updated to ${status}`);
    } catch (error) {
      toast.error('Failed to update status');
    }
  };

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

  if (loading) return <LoadingSpinner />;
  if (!ticket) return null;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <button
        onClick={() => navigate('/tickets')}
        className="mb-4 flex items-center space-x-2 text-gray-600 hover:text-gray-900"
      >
        <FiArrowLeft className="h-5 w-5" />
        <span>Back to Tickets</span>
      </button>

      <div className="card mb-6">
        <div className="flex justify-between items-start mb-4">
          <h1 className="text-2xl font-bold text-gray-900">{ticket.title}</h1>
          <div className="flex space-x-2">
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColors[ticket.status]}`}>
              {ticket.status.replace('_', ' ')}
            </span>
            <span className={`px-2 py-1 text-xs font-medium rounded-full ${priorityColors[ticket.priority]}`}>
              {ticket.priority}
            </span>
          </div>
        </div>

        <p className="text-gray-700 mb-4 whitespace-pre-wrap">{ticket.description}</p>

        <div className="flex items-center text-sm text-gray-500 space-x-4">
          <div className="flex items-center space-x-1">
            <FiClock className="h-4 w-4" />
            <span>Created: {new Date(ticket.created_at).toLocaleString()}</span>
          </div>
          <div className="flex items-center space-x-1">
            <FiTag className="h-4 w-4" />
            <span>ID: #{ticket.ticket_id}</span>
          </div>
        </div>

        {user?.is_admin && (
          <div className="mt-4 pt-4 border-t">
            <label className="block text-sm font-medium text-gray-700 mb-2">Update Status</label>
            <div className="flex space-x-2">
              {['open', 'in_progress', 'resolved', 'closed'].map(status => (
                <button
                  key={status}
                  onClick={() => updateTicketStatus(status)}
                  className={`px-3 py-1 text-sm rounded-full ${
                    ticket.status === status
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {status.replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* AI Suggestion */}
      {aiSuggestion && aiSuggestion.confidence_score > 0.6 && !showAISuggestion && (
        <div className="card mb-6 bg-blue-50 border-blue-200">
          <div className="flex items-start space-x-3">
            <FiBot className="h-6 w-6 text-blue-500" />
            <div className="flex-1">
              <h3 className="font-semibold text-gray-900 mb-2">AI Suggested Reply</h3>
              <p className="text-gray-700 mb-3">{aiSuggestion.suggested_reply}</p>
              <div className="flex space-x-2">
                <button
                  onClick={handleUseAISuggestion}
                  className="btn-primary text-sm py-1 px-3"
                >
                  Use this reply
                </button>
                <button
                  onClick={() => setShowAISuggestion(true)}
                  className="btn-secondary text-sm py-1 px-3"
                >
                  Dismiss
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Replies */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
          <FiMessageSquare className="h-5 w-5" />
          <span>Conversation ({replies.length} replies)</span>
        </h2>

        <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
          {replies.map((reply) => (
            <div
              key={reply.reply_id}
              className={`flex ${reply.sender_type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] rounded-lg p-3 ${
                  reply.sender_type === 'user'
                    ? 'bg-primary-600 text-white'
                    : reply.sender_type === 'AI'
                    ? 'bg-blue-100 text-gray-900'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <div className="flex items-center space-x-2 mb-1">
                  <FiUser className="h-3 w-3" />
                  <span className="text-xs font-medium">
                    {reply.sender_type === 'user' ? 'You' : reply.sender_type === 'AI' ? 'AI Assistant' : 'Support Agent'}
                  </span>
                  <span className="text-xs opacity-75">
                    {new Date(reply.created_at).toLocaleString()}
                  </span>
                </div>
                <p className="text-sm whitespace-pre-wrap">{reply.message}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="border-t pt-4">
          <textarea
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type your reply..."
            rows="3"
            className="input-field mb-3"
          />
          <div className="flex justify-end">
            <button
              onClick={handleSendReply}
              disabled={sending || !newMessage.trim()}
              className="btn-primary flex items-center space-x-2"
            >
              <FiSend className="h-4 w-4" />
              <span>{sending ? 'Sending...' : 'Send Reply'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TicketDetail;