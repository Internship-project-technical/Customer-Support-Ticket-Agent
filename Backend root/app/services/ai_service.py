import httpx
import json
from typing import Optional, Dict, Any, List
from ..config import settings

class AIService:
    def __init__(self):
        self.base_url = settings.LLAMA_BASE_URL
        self.model = settings.LLAMA_MODEL

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Generate a response using the Llama model"""
        
        # Prepare full prompt with context if available
        full_prompt = prompt
        if context:
            full_prompt = f"""Context: {context}

User Query: {prompt}

Please provide a helpful and professional response:"""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={
                        "model": self.model,
                        "prompt": full_prompt,
                        "stream": False,
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "response": data.get("response", ""),
                        "model": self.model
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API returned status {response.status_code}",
                        "response": "I apologize, but I'm having trouble processing your request right now."
                    }
                    
        except Exception as e:
            print(f"AI Service Error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I'm currently experiencing technical difficulties. Please try again later."
            }

    async def triage_ticket(self, title: str, description: str) -> Dict[str, Any]:
        """Auto-categorize and prioritize incoming ticket"""
        
        prompt = f"""You are a customer support ticket triage system. Analyze this ticket and return a JSON response.

Ticket Title: {title}
Ticket Description: {description}

Return a JSON object with:
- category: one of [billing, technical, account, feature_request, general]
- subcategory: more specific sub-category (e.g., login_issue, payment_failed)
- priority: one of [P1, P2, P3, P4] (P1=urgent/critical, P4=low priority)
- sentiment: one of [positive, neutral, negative]
- suggested_department: one of [billing, technical_support, account_management, product]

Only return valid JSON, no other text."""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = json.loads(data.get("response", "{}"))
                    return {
                        "success": True,
                        "category": result.get("category", "general"),
                        "subcategory": result.get("subcategory"),
                        "priority": result.get("priority", "P3"),
                        "sentiment": result.get("sentiment", "neutral"),
                        "suggested_department": result.get("suggested_department", "general")
                    }
        except Exception as e:
            print(f"AI Triage Error: {e}")
        
        # Default response if AI fails
        return {
            "success": False,
            "category": "general",
            "subcategory": None,
            "priority": "P3",
            "sentiment": "neutral",
            "suggested_department": "general"
        }

    async def suggest_reply(self, ticket_title: str, ticket_description: str, ticket_category: Optional[str] = None) -> Dict[str, Any]:
        """Generate AI-suggested reply for a ticket"""
        
        prompt = f"""You are a customer support agent. Generate a helpful, professional reply for this support ticket.

Ticket Title: {ticket_title}
Ticket Description: {ticket_description}
{f'Category: {ticket_category}' if ticket_category else ''}

Please provide a friendly, helpful response that addresses the customer's issue. Be concise but thorough."""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": 0.8,
                        "max_tokens": 300
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "suggested_reply": data.get("response", ""),
                        "confidence_score": 0.85
                    }
        except Exception as e:
            print(f"AI Reply Error: {e}")
        
        return {
            "success": False,
            "suggested_reply": "Thank you for reaching out. Our team will review your ticket and get back to you shortly.",
            "confidence_score": 0.5
        }

    async def extract_faq(self, ticket_title: str, ticket_description: str, resolution: str) -> Optional[Dict[str, str]]:
        """Extract Q&A pair from resolved ticket for FAQ"""
        
        prompt = f"""Based on this resolved customer support ticket, extract a potential FAQ question and answer.

Ticket Title: {ticket_title}
Issue: {ticket_description}
Resolution: {resolution}

Return a JSON object with:
- question: a clear, concise question that customers would ask
- answer: the solution/answer to the question

Only return valid JSON, no other text."""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = json.loads(data.get("response", "{}"))
                    return {
                        "question": result.get("question"),
                        "answer": result.get("answer")
                    }
        except Exception as e:
            print(f"FAQ Extraction Error: {e}")
        
        return None

# Create singleton instance
ai_service = AIService()
