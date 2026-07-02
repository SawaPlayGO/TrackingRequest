from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from database import async_session
from repo.ticket_repo import TicketRepo


class IUnitOfWork(ABC):
    ticket_repo: TicketRepo

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError
    

class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession] = async_session):
        self._session_factory = session_factory

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        
        self.ticket_repo = TicketRepo(self._session)
        return await super().__aenter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def flush(self) -> None:
        await self._session.flush()