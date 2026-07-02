import math

from utils.enums import TicketStatus
from models.tickets import Ticket
from schemes.tickets import (
    TicketCreate,
    TicketListResponse,
    TicketPaginationQueryParams,
    TicketResponse,
    TicketStatusUpdate,
)

from utils.uow import IUnitOfWork
from utils.logging import logger


class TicketService:
    @staticmethod
    async def create(uow: IUnitOfWork, ticket: TicketCreate) -> TicketResponse:
        async with uow:
            new_ticket: Ticket | None = await uow.ticket_repo.create(
                title=ticket.title,
                status=ticket.status,
                priority=ticket.priority,
                description=ticket.description,
            )
            if new_ticket is None:
                await logger.aerror("Failed to create ticket")
                raise ValueError("Failed to create ticket")
            return TicketResponse.model_validate(new_ticket)

    @staticmethod
    async def get_list(
        uow: IUnitOfWork, params: TicketPaginationQueryParams
    ) -> TicketListResponse:
        offset = TicketService._calculate_offset(page=params.page, limit=params.limit)

        async with uow:
            tickets_models = await uow.ticket_repo.get_list(
                limit=params.limit,
                offset=offset,
                status=params.status,
                priority=params.priority,
                sort_by_date=params.sort_by_date.value,
                sort_by_priority=params.sort_by_priority.value
                if params.sort_by_priority
                else None,
                search=params.search,
            )

            total_count = await uow.ticket_repo.count(
                status=params.status, priority=params.priority, search=params.search
            )

        ticket_responses = [
            TicketResponse.model_validate(ticket) for ticket in tickets_models
        ]
        total_pages = TicketService._calculate_total_pages(total_count, params.limit)

        return TicketListResponse(
            items=ticket_responses,
            total=total_count,
            page=params.page,
            limit=params.limit,
            pages=total_pages,
        )

    @staticmethod
    async def update_status(
        uow: IUnitOfWork, ticket_id: int, payload: TicketStatusUpdate
    ) -> TicketResponse:
        async with uow:
            ticket = await uow.ticket_repo.get_by_id(ticket_id)
            if not ticket:
                raise KeyError(f"Заявка с ID {ticket_id} не найдена")

            TicketService._validate_status_transition(
                current_status=ticket.status, new_status=payload.status
            )

            updated_ticket = await uow.ticket_repo.update_status(
                ticket_id=ticket_id, new_status=payload.status
            )

            await uow.flush()
            response = TicketResponse.model_validate(updated_ticket)
            await uow.commit()

            return response

    @staticmethod
    async def delete_ticket(uow: IUnitOfWork, ticket_id: int) -> None:
        async with uow:
            ticket = await uow.ticket_repo.get_by_id(ticket_id)
            if not ticket:
                raise KeyError(f"Ticket with ID {ticket_id} not found")

            if ticket.status == TicketStatus.DONE:
                await logger.aerror(
                    f"Cannot delete a ticket with ID {ticket_id} that is already DONE"
                )
                raise ValueError("Cannot delete a ticket with status DONE")

            await uow.ticket_repo.delete(ticket_id)

            await uow.flush()
            await uow.commit()

    @staticmethod
    def _calculate_offset(page: int, limit: int) -> int:
        """Вспомогательный метод для расчета смещения (offset) в SQL"""
        return (page - 1) * limit

    @staticmethod
    def _calculate_total_pages(total_count: int, limit: int) -> int:
        """Вспомогательный метод для расчета общего количества страниц"""
        if total_count == 0:
            return 1
        return math.ceil(total_count / limit)

    @staticmethod
    def _validate_status_transition(
        current_status: TicketStatus, new_status: TicketStatus
    ) -> None:
        """Проверка бизнес-правил перехода из статуса в статус"""
        if current_status == TicketStatus.DONE:
            logger.error("Cannot change status of a ticket that is already DONE")
            raise ValueError("Cannot change status of a ticket that is already DONE")
