# Add this to the end of your schemas.py file

# AI Schemas
class AITriageResponse(BaseModel):
    category: str
    subcategory: Optional[str] = None
    priority: str
    sentiment: str
    suggested_department: str

class AIReplyResponse(BaseModel):
    suggested_reply: str
    confidence_score: float
    is_faq_based: bool = False
    faq_id: Optional[int] = None

class AIRequest(BaseModel):
    message: str
    ticket_id: Optional[int] = None
    context: Optional[str] = None

class AIResponse(BaseModel):
    response: str
    suggested_actions: Optional[List[str]] = None
