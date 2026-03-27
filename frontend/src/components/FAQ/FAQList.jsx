import React, { useState, useEffect } from 'react';
import { faqAPI } from '../../services/api';
import { FiSearch, FiChevronDown, FiChevronUp } from 'react-icons/fi';
import LoadingSpinner from '../Common/LoadingSpinner';

const FAQList = () => {
  const [faqs, setFaqs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    fetchFaqs();
  }, []);

  const fetchFaqs = async () => {
    try {
      const response = await faqAPI.getAll();
      setFaqs(response.data);
    } catch (error) {
      console.error('Failed to fetch FAQs:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredFaqs = faqs.filter(faq =>
    faq.question.toLowerCase().includes(search.toLowerCase()) ||
    faq.answer.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Frequently Asked Questions</h1>
      <p className="text-gray-600 mb-6">Find answers to common questions about our support system</p>

      <div className="relative mb-8">
        <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search FAQs..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="input-field pl-10"
        />
      </div>

      {filteredFaqs.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No FAQs found matching your search</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredFaqs.map((faq) => (
            <div key={faq.faq_id} className="card">
              <button
                onClick={() => setExpandedId(expandedId === faq.faq_id ? null : faq.faq_id)}
                className="w-full flex justify-between items-center text-left"
              >
                <h3 className="text-lg font-semibold text-gray-900">{faq.question}</h3>
                {expandedId === faq.faq_id ? (
                  <FiChevronUp className="h-5 w-5 text-gray-500" />
                ) : (
                  <FiChevronDown className="h-5 w-5 text-gray-500" />
                )}
              </button>
              {expandedId === faq.faq_id && (
                <div className="mt-4 pt-4 border-t">
                  <p className="text-gray-700 whitespace-pre-wrap">{faq.answer}</p>
                  {faq.times_used > 0 && (
                    <p className="text-xs text-gray-400 mt-2">Helped {faq.times_used} people</p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FAQList;