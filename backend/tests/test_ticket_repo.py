import unittest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database import Base
from repo.ticket_repo import TicketRepo
from utils.enums import TicketPriority, TicketStatus


class TicketRepoTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
        self.Session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def asyncTearDown(self):
        await self.engine.dispose()

    async def test_create_and_get_by_id(self):
        async with self.Session() as session:
            repo = TicketRepo(session)
            created = await repo.create(
                title="title",
                status=TicketStatus.NEW,
                priority=TicketPriority.HIGH,
                description="desc",
            )
            await session.commit()

            self.assertIsNotNone(created.id)
            fetched = await repo.get_by_id(created.id)
            self.assertEqual(fetched.id, created.id)
            self.assertEqual(fetched.title, "title")

    async def test_get_list_with_filters_and_search(self):
        async with self.Session() as session:
            repo = TicketRepo(session)
            await repo.create(
                title="Hello world",
                status=TicketStatus.NEW,
                priority=TicketPriority.NORMAL,
                description="Search this text",
            )
            await repo.create(
                title="Another",
                status=TicketStatus.IN_PROGRESS,
                priority=TicketPriority.HIGH,
                description="Other",
            )
            await session.commit()

            results = await repo.get_list(
                limit=10,
                offset=0,
                status=TicketStatus.NEW,
                priority=TicketPriority.NORMAL,
                sort_by_date="desc",
                sort_by_priority=None,
                search="search",
            )
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].title, "Hello world")

    async def test_count_with_filters(self):
        async with self.Session() as session:
            repo = TicketRepo(session)
            await repo.create(
                title="Count me",
                status=TicketStatus.NEW,
                priority=TicketPriority.LOW,
            )
            await session.commit()

            count = await repo.count(status=TicketStatus.NEW)
            self.assertEqual(count, 1)

    async def test_update_status_and_delete(self):
        async with self.Session() as session:
            repo = TicketRepo(session)
            ticket = await repo.create(
                title="To update",
                status=TicketStatus.NEW,
                priority=TicketPriority.NORMAL,
            )
            await session.commit()

            updated = await repo.update_status(
                ticket_id=ticket.id, new_status=TicketStatus.IN_PROGRESS
            )
            self.assertEqual(updated.status, TicketStatus.IN_PROGRESS)

            deleted = await repo.delete(ticket.id)
            self.assertTrue(deleted)
            await session.commit()

            missing = await repo.get_by_id(ticket.id)
            self.assertIsNone(missing)
