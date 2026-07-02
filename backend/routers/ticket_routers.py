from fastapi import APIRouter, Depends, HTTPException, status

from services.ticket_services import TicketService
from utils.uow import IUnitOfWork
from utils.depend import get_ticket_service, get_uow
from schemes.tickets import (
    TicketCreate,
    TicketListResponse,
    TicketPaginationQueryParams,
    TicketResponse,
    TicketStatusUpdate,
)

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket: TicketCreate,
    uow: IUnitOfWork = Depends(get_uow),
    ticket_service: TicketService = Depends(get_ticket_service),
) -> TicketResponse:
    try:
        response_ticket: TicketResponse = await ticket_service.create(
            uow=uow, ticket=ticket
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"status": "error"}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error"},
        )

    return response_ticket


@router.get(
    "/",
    response_model=TicketListResponse,
    description="Получить список заявок с пагинацией и фильтрацией",
)
async def get_tickets_list(
    params: TicketPaginationQueryParams = Depends(),
    uow: IUnitOfWork = Depends(get_uow),
    ticket_service: TicketService = Depends(get_ticket_service),
) -> TicketListResponse:

    try:
        result: TicketListResponse = await ticket_service.get_list(
            uow=uow, params=params
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error"},
        )
    return result


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
    description="Обновить статус заявки с проверкой бизнес-правил",
)
async def update_ticket_status(
    ticket_id: int,
    payload: TicketStatusUpdate,
    uow: IUnitOfWork = Depends(get_uow),
    ticket_service: TicketService = Depends(get_ticket_service),
) -> TicketResponse:
    try:
        updated_ticket = await ticket_service.update_status(
            uow=uow, ticket_id=ticket_id, payload=payload
        )
        return updated_ticket

    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"reason": str(e)}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error"},
        )


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить заявку по её ID (нельзя удалять в статусе DONE)",
)
async def delete_ticket(
    ticket_id: int,
    uow: IUnitOfWork = Depends(get_uow),
    ticket_service: TicketService = Depends(get_ticket_service),
) -> None:
    try:
        await ticket_service.delete_ticket(uow=uow, ticket_id=ticket_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"reason": str(e)}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error"},
        )
