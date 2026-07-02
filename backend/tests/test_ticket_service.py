import unittest
from datetime import datetime, timezone

from services.ticket_services import TicketService
from schemes.tickets import TicketCreate, TicketPaginationQueryParams, TicketStatusUpdate
from utils.enums import TicketPriority, TicketStatus, SortTicket
from models.tickets import Ticket


class DummyTicketRepo:
    def __init__(
        self,
        create_return=None,
        list_return=None,
        count_return=0,
        get_by_id_return=None,
        update_status_return=None,
        delete_return=False,
    ):
        self.create_return = create_return
        self.list_return = list_return or []
        self.count_return = count_return
        self.get_by_id_return = get_by_id_return
        self.update_status_return = update_status_return
        self.delete_return = delete_return
        self.create_called = False
        self.get_list_called = False
        self.count_called = False
        self.get_by_id_called = False
        self.update_status_called = False
        self.delete_called = False
        self.create_args = None
        self.get_list_args = None
        self.count_args = None
        self.update_status_args = None
        self.delete_args = None

    async def create(self, *, title, status, priority, description=None):
        self.create_called = True
        self.create_args = dict(title=title, status=status, priority=priority, description=description)
        return self.create_return

    async def get_list(
        self,
        *,
        limit,
        offset,
        status=None,
        priority=None,
        sort_by_date="desc",
        sort_by_priority=None,
        search=None,
    ):
        self.get_list_called = True
        self.get_list_args = dict(
            limit=limit,
            offset=offset,
            status=status,
            priority=priority,
            sort_by_date=sort_by_date,
            sort_by_priority=sort_by_priority,
            search=search,
        )
        return self.list_return

    async def count(self, *, status=None, priority=None, search=None):
        self.count_called = True
        self.count_args = dict(status=status, priority=priority, search=search)
        return self.count_return

    async def update_status(self, *, ticket_id, new_status):
        self.update_status_called = True
        self.update_status_args = dict(ticket_id=ticket_id, new_status=new_status)
        return self.update_status_return

    async def get_by_id(self, ticket_id):
        self.get_by_id_called = True
        self.get_by_id_args = dict(ticket_id=ticket_id)
        return self.get_by_id_return

    async def delete(self, ticket_id):
        self.delete_called = True
        self.delete_args = dict(ticket_id=ticket_id)
        return self.delete_return


class DummyUnitOfWork:
    def __init__(self, repo):
        self.ticket_repo = repo
        self.commit_called = False
        self.rollback_called = False
        self.flush_called = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False

    async def commit(self):
        self.commit_called = True

    async def rollback(self):
        self.rollback_called = True

    async def flush(self):
        self.flush_called = True


def make_ticket(**kwargs) -> Ticket:
    return Ticket(
        id=kwargs.get("id", 1),
        title=kwargs.get("title", "Test title"),
        description=kwargs.get("description", "Test description"),
        status=kwargs.get("status", TicketStatus.NEW),
        priority=kwargs.get("priority", TicketPriority.NORMAL),
        created_at=kwargs.get("created_at", datetime.now(timezone.utc)),
        updated_at=kwargs.get("updated_at", datetime.now(timezone.utc)),
    )


class TicketServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_create_ticket_success(self):
        ticket = make_ticket()
        repo = DummyTicketRepo(create_return=ticket)
        uow = DummyUnitOfWork(repo)

        payload = TicketCreate(
            title="Заявка",
            description="Описание",
            status=TicketStatus.NEW,
            priority=TicketPriority.HIGH,
        )

        response = await TicketService.create(uow, payload)

        self.assertEqual(response.id, ticket.id)
        self.assertEqual(response.title, ticket.title)
        self.assertTrue(repo.create_called)
        self.assertEqual(repo.create_args["title"], "Заявка")

    async def test_create_ticket_raises_when_repo_returns_none(self):
        repo = DummyTicketRepo(create_return=None)
        uow = DummyUnitOfWork(repo)

        payload = TicketCreate(
            title="Заявка",
            description="Описание",
            status=TicketStatus.NEW,
            priority=TicketPriority.NORMAL,
        )

        with self.assertRaises(ValueError):
            await TicketService.create(uow, payload)

    async def test_get_list_returns_pagination_response(self):
        ticket = make_ticket(id=10)
        repo = DummyTicketRepo(list_return=[ticket], count_return=1)
        uow = DummyUnitOfWork(repo)

        params = TicketPaginationQueryParams(
            page=1,
            limit=10,
            status=TicketStatus.NEW,
            priority=TicketPriority.NORMAL,
            sort_by_date=SortTicket.DESC,
            sort_by_priority=None,
            search="test",
        )

        response = await TicketService.get_list(uow, params)

        self.assertEqual(response.total, 1)
        self.assertEqual(response.pages, 1)
        self.assertEqual(response.page, 1)
        self.assertEqual(response.limit, 10)
        self.assertEqual(len(response.items), 1)
        self.assertTrue(repo.get_list_called)
        self.assertTrue(repo.count_called)
        self.assertEqual(repo.get_list_args["offset"], 0)

    async def test_update_status_success(self):
        ticket = make_ticket(status=TicketStatus.NEW)
        updated = make_ticket(status=TicketStatus.IN_PROGRESS)
        repo = DummyTicketRepo(get_by_id_return=ticket, update_status_return=updated)
        uow = DummyUnitOfWork(repo)

        response = await TicketService.update_status(
            uow,
            ticket_id=1,
            payload=TicketStatusUpdate(status=TicketStatus.IN_PROGRESS),
        )

        self.assertEqual(response.status, TicketStatus.IN_PROGRESS)
        self.assertTrue(repo.get_by_id_called)
        self.assertTrue(repo.update_status_called)
        self.assertTrue(uow.flush_called)
        self.assertTrue(uow.commit_called)

    async def test_update_status_raises_key_error_when_ticket_missing(self):
        repo = DummyTicketRepo(get_by_id_return=None)
        uow = DummyUnitOfWork(repo)

        with self.assertRaises(KeyError):
            await TicketService.update_status(
                uow,
                ticket_id=999,
                payload=TicketStatusUpdate(status=TicketStatus.IN_PROGRESS),
            )

    async def test_update_status_raises_value_error_when_ticket_done(self):
        ticket = make_ticket(status=TicketStatus.DONE)
        repo = DummyTicketRepo(get_by_id_return=ticket)
        uow = DummyUnitOfWork(repo)

        with self.assertRaises(ValueError):
            await TicketService.update_status(
                uow,
                ticket_id=1,
                payload=TicketStatusUpdate(status=TicketStatus.NEW),
            )

    async def test_delete_ticket_success(self):
        ticket = make_ticket(status=TicketStatus.IN_PROGRESS)
        repo = DummyTicketRepo(get_by_id_return=ticket, delete_return=True)
        uow = DummyUnitOfWork(repo)

        await TicketService.delete_ticket(uow, ticket_id=1)

        self.assertTrue(repo.get_by_id_called)
        self.assertTrue(repo.delete_called)
        self.assertTrue(uow.flush_called)
        self.assertTrue(uow.commit_called)

    async def test_delete_ticket_raises_key_error_when_ticket_missing(self):
        repo = DummyTicketRepo(get_by_id_return=None)
        uow = DummyUnitOfWork(repo)

        with self.assertRaises(KeyError):
            await TicketService.delete_ticket(uow, ticket_id=999)

    async def test_delete_ticket_raises_value_error_when_ticket_done(self):
        ticket = make_ticket(status=TicketStatus.DONE)
        repo = DummyTicketRepo(get_by_id_return=ticket)
        uow = DummyUnitOfWork(repo)

        with self.assertRaises(ValueError):
            await TicketService.delete_ticket(uow, ticket_id=1)

    def test_calculate_offset_and_total_pages(self):
        self.assertEqual(TicketService._calculate_offset(page=1, limit=10), 0)
        self.assertEqual(TicketService._calculate_offset(page=3, limit=5), 10)
        self.assertEqual(TicketService._calculate_total_pages(total_count=0, limit=10), 1)
        self.assertEqual(TicketService._calculate_total_pages(total_count=21, limit=10), 3)
