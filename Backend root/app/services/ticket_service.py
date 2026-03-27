from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from .. import models, schemas

class TicketService:
    @staticmethod
    def create_ticket(db: Session, ticket: schemas.TicketCreate, user_id: Optional[int] = None) -> models.Ticket:
        # Handle user creation if email provided
        if ticket.email and not user_id:
            user = db.query(models.User).filter(models.User.email == ticket.email).first()
            if not user:
                user = models.User(
                    name=ticket.name or ticket.email.split('@')[0],
                    email=ticket.email,
                    phone=None
                )
                db.add(user)
                db.flush()
                user_id = user.user_id
        
        db_ticket = models.Ticket(
            user_id=user_id,
            title=ticket.title,
            description=ticket.description,
            status=models.StatusEnum.open,
            ai_suggestion_used=False
        )
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket

    @staticmethod
    def get_tickets(db: Session, skip: int = 0, limit: int = 100, 
                    status: Optional[str] = None, category: Optional[str] = None,
                    assigned_agent_id: Optional[int] = None) -> List[models.Ticket]:
        query = db.query(models.Ticket)
        
        if status:
            query = query.filter(models.Ticket.status == status)
        if category:
            query = query.join(models.Category).filter(models.Category.category_name == category)
        if assigned_agent_id:
            query = query.filter(models.Ticket.assigned_agent_id == assigned_agent_id)
        
        return query.offset(skip).limit(limit).order_by(
            models.Ticket.priority.asc(),
            models.Ticket.created_at.asc()
        ).all()

    @staticmethod
    def get_ticket(db: Session, ticket_id: int) -> models.Ticket:
        return db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()

    @staticmethod
    def update_ticket(db: Session, ticket_id: int, ticket_update: schemas.TicketUpdate) -> models.Ticket:
        db_ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
        if db_ticket:
            for key, value in ticket_update.dict(exclude_unset=True).items():
                setattr(db_ticket, key, value)
            
            # Update resolution time if status changed to resolved
            if ticket_update.status == "resolved" and db_ticket.status != "resolved":
                db_ticket.resolved_at = datetime.now()
                if db_ticket.created_at:
                    resolution_time = datetime.now() - db_ticket.created_at
                    db_ticket.resolution_time_minutes = resolution_time.total_seconds() / 60
            
            db.commit()
            db.refresh(db_ticket)
        return db_ticket

    @staticmethod
    def add_reply(db: Session, ticket_id: int, message: str, sender_type: str) -> models.TicketReply:
        reply = models.TicketReply(
            ticket_id=ticket_id,
            message=message,
            sender_type=sender_type
        )
        db.add(reply)
        db.commit()
        db.refresh(reply)
        return reply

    @staticmethod
    def get_analytics(db: Session) -> schemas.TicketAnalytics:
        total = db.query(models.Ticket).count()
        open_tickets = db.query(models.Ticket).filter(models.Ticket.status == "open").count()
        in_progress = db.query(models.Ticket).filter(models.Ticket.status == "in-progress").count()
        resolved = db.query(models.Ticket).filter(models.Ticket.status == "resolved").count()
        
        # Average resolution time
        avg_resolution = db.query(func.avg(models.Ticket.resolution_time_minutes)).filter(
            models.Ticket.resolution_time_minutes.isnot(None)
        ).scalar()
        
        # Category distribution
        categories = db.query(
            models.Category.category_name,
            func.count(models.Ticket.ticket_id)
        ).outerjoin(models.Ticket).group_by(models.Category.category_id).all()
        category_dist = {cat: count for cat, count in categories}
        
        # Priority distribution
        priorities = db.query(
            models.Ticket.priority,
            func.count(models.Ticket.ticket_id)
        ).group_by(models.Ticket.priority).all()
        priority_dist = {pri: count for pri, count in priorities}
        
        # AI suggestion acceptance rate
        ai_used = db.query(models.Ticket).filter(models.Ticket.ai_suggestion_used == True).count()
        acceptance_rate = (ai_used / total * 100) if total > 0 else 0
        
        return schemas.TicketAnalytics(
            total_tickets=total,
            open_tickets=open_tickets,
            in_progress_tickets=in_progress,
            resolved_tickets=resolved,
            avg_resolution_time_minutes=avg_resolution,
            category_distribution=category_dist,
            priority_distribution=priority_dist,
            ai_suggestion_acceptance_rate=acceptance_rate
        )

ticket_service = TicketService()