import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from services.ticket_services import TicketService
from utils.uow import IUnitOfWork, UnitOfWork
from config import settings

security_schema = HTTPBasic()


async def get_uow() -> IUnitOfWork:
    return UnitOfWork()


async def get_ticket_service() -> TicketService:
    return TicketService()


async def verify_admin(credentials: HTTPBasicCredentials = Depends(security_schema)):
    correct_username = secrets.compare_digest(credentials.username, settings.ADMIN_USER)
    correct_password = secrets.compare_digest(credentials.password, settings.ADMIN_PASS)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
