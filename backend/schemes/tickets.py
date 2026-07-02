from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from utils.enums import SortTicket, TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=120,
        description="Название заявки",
    )

    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Подробное описание заявки",
    )

    status: TicketStatus = Field(..., description="Текущий статус заявки")

    priority: TicketPriority = Field(..., description="Приоритет заявки")


class TicketResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketPaginationQueryParams(BaseModel):
    page: int = Field(1, ge=1, description="Номер страницы (начиная с 1)")
    limit: int = Field(10, ge=1, le=100, description="Количество элементов на странице")

    status: Optional[TicketStatus] = Field(None, description="Фильтр по статусу заявки")
    priority: Optional[TicketPriority] = Field(None, description="Фильтр по приоритету")

    sort_by_date: SortTicket = Field(
        SortTicket.DESC, description="Сортировка по дате создания (asc/desc)"
    )
    sort_by_priority: Optional[SortTicket] = Field(
        None,
        description="Сортировка по приоритету (asc/desc). Если не указана, не применяется.",
    )

    search: Optional[str] = Field(
        None, min_length=1, description="Поиск по названию или описанию заявки"
    )


class TicketListResponse(BaseModel):
    items: list[TicketResponse] = Field(
        ..., description="Список заявок на текущей странице"
    )

    total: int = Field(
        ..., description="Общее количество заявок в базе по заданным фильтрам"
    )
    page: int = Field(..., description="Текущая страница")
    limit: int = Field(..., description="Количество элементов на странице")
    pages: int = Field(..., description="Общее количество страниц")


class TicketStatusUpdate(BaseModel):
    status: TicketStatus = Field(..., description="Новый статус для заявки")
