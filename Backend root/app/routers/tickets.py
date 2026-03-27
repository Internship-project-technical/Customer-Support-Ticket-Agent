from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models
from ..database import get_db
from ..dependencies import get_current_user
from ..services.ai_service import ai_service

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/", response_model=schemas.Ticket)
def create_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new support ticket"""
    # Create ticket
    db_ticket = models.Ticket(
        user_id=current_user.user_id,
        title=ticket.title,
        description=ticket.description,
        status=models.StatusEnum.open,
        priority=models.PriorityEnum.P3
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    return db_ticket

@router.get("/", response_model=List[schemas.Ticket])
def get_tickets(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all tickets for current user (admin gets all)"""
    query = db.query(models.Ticket)
    
    # If not admin, only show user's own tickets
    if not current_user.is_admin:
        query = query.filter(models.Ticket.user_id == current_user.user_id)
    
    if status:
        query = query.filter(models.Ticket.status == status)
    
    return query.order_by(models.Ticket.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{ticket_id}", response_model=schemas.Ticket)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a specific ticket"""
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Check if user has access to this ticket
    if not current_user.is_admin and ticket.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")
    
    return ticket

@router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(
    ticket_id: int,
    ticket_update: schemas.TicketUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a ticket"""
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Check if user has access to update this ticket
    if not current_user.is_admin and ticket.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this ticket")
    
    # Update fields
    update_data = ticket_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    db.commit()
    db.refresh(ticket)
    return ticket

@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a ticket (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db.delete(ticket)
    db.commit()
    return {"message": "Ticket deleted successfully"}

@router.get("/analytics", response_model=dict)
def get_ticket_analytics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get ticket analytics"""
    # Admin only
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    total = db.query(models.Ticket).count()
    open_tickets = db.query(models.Ticket).filter(models.Ticket.status == models.StatusEnum.open).count()
    in_progress = db.query(models.Ticket).filter(models.Ticket.status == models.StatusEnum.in_progress).count()
    resolved = db.query(models.Ticket).filter(models.Ticket.status == models.StatusEnum.resolved).count()
    
    return {
        "total_tickets": total,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress,
        "resolved_tickets": resolved
    }
