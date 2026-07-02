from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.tickets import Ticket
from utils.enums import TicketPriority, TicketStatus


class TicketRepo:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, *, title: str, status: TicketStatus, priority: TicketPriority, description: str | None = None) -> Ticket | None:
        ticket = Ticket(
            title=title,
            status=status,
            priority=priority,
            description=description
        )
        self._session.add(ticket)
        await self._session.flush()
        return ticket
    
    async def get_list(
        self, 
        *,
        limit: int, 
        offset: int, 
        status: TicketStatus | None = None, 
        priority: TicketPriority | None = None,
        sort_by_date: str = "desc",
        sort_by_priority: str | None = None,
        search: str | None = None
    ) -> list[Ticket]:
        query = select(Ticket)
        
        if status is not None:
            query = query.where(Ticket.status == status)
        if priority is not None:
            query = query.where(Ticket.priority == priority)
            
        if search is not None:
            search_expr = f"%{search}%"
            query = query.where(
                or_(
                    Ticket.title.ilike(search_expr),
                    Ticket.description.ilike(search_expr)
                )
            )
            
        order_fields = []
        if sort_by_priority is not None:
            order_fields.append(Ticket.priority.desc() if sort_by_priority == "desc" else Ticket.priority.asc())
        order_fields.append(Ticket.created_at.desc() if sort_by_date == "desc" else Ticket.created_at.asc())
        
        query = query.order_by(*order_fields).limit(limit).offset(offset)
            
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def count(
        self, 
        *,
        status: TicketStatus | None = None, 
        priority: TicketPriority | None = None,
        search: str | None = None
    ) -> int:
        query = select(func.count(Ticket.id))
        
        if status is not None:
            query = query.where(Ticket.status == status)
        if priority is not None:
            query = query.where(Ticket.priority == priority)
            
        if search is not None:
            search_expr = f"%{search}%"
            query = query.where(
                or_(
                    Ticket.title.ilike(search_expr),
                    Ticket.description.ilike(search_expr)
                )
            )
            
        result = await self._session.execute(query)
        return result.scalar_one()
    
    async def update_status(self, *, ticket_id: int, new_status: TicketStatus) -> Ticket | None:
        ticket = await self.get_by_id(ticket_id)
        if ticket:
            ticket.status = new_status
        return ticket
    
    async def get_by_id(self, ticket_id: int) -> Ticket | None:
        query = select(Ticket).where(Ticket.id == ticket_id)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
    
    async def delete(self, ticket_id: int) -> bool:
        ticket = await self.get_by_id(ticket_id)
        if ticket:
            await self._session.delete(ticket)
            return True
        return False