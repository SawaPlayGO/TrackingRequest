from services.ticket_services import TicketService
from utils.uow import IUnitOfWork, UnitOfWork


async def get_uow() -> IUnitOfWork:
    return UnitOfWork()


async def get_ticket_service() -> TicketService:
    return TicketService()
