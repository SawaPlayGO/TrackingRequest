import unittest
from unittest.mock import AsyncMock

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from routers import ticket_routers


class DummyUoW:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False


class TicketRouterTest(unittest.TestCase):
    def setUp(self):
        app.dependency_overrides.clear()
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_create_ticket_returns_201(self):
        service = AsyncMock()
        service.create.return_value = {
            "id": 1,
            "title": "Заявка",
            "description": "Описание",
            "status": "new",
            "priority": "normal",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }

        app.dependency_overrides[ticket_routers.get_ticket_service] = lambda: service
        app.dependency_overrides[ticket_routers.get_uow] = lambda: DummyUoW()

        response = self.client.post(
            "/tickets/",
            json={
                "title": "Заявка",
                "description": "Описание",
                "status": "new",
                "priority": "normal",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tickets_list_returns_200(self):
        service = AsyncMock()
        service.get_list.return_value = {
            "items": [],
            "total": 0,
            "page": 1,
            "limit": 10,
            "pages": 1,
        }

        app.dependency_overrides[ticket_routers.get_ticket_service] = lambda: service
        app.dependency_overrides[ticket_routers.get_uow] = lambda: DummyUoW()

        response = self.client.get("/tickets/?page=1&limit=10")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ticket_status_returns_200(self):
        service = AsyncMock()
        service.update_status.return_value = {
            "id": 1,
            "title": "Тест",
            "description": None,
            "status": "in_progress",
            "priority": "normal",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }

        app.dependency_overrides[ticket_routers.get_ticket_service] = lambda: service
        app.dependency_overrides[ticket_routers.get_uow] = lambda: DummyUoW()

        response = self.client.patch(
            "/tickets/1/status",
            json={"status": "in_progress"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ticket_returns_204(self):
        service = AsyncMock()
        service.delete_ticket.return_value = None

        app.dependency_overrides[ticket_routers.get_ticket_service] = lambda: service
        app.dependency_overrides[ticket_routers.get_uow] = lambda: DummyUoW()
        app.dependency_overrides[ticket_routers.verify_admin] = lambda: "admin"

        response = self.client.delete("/tickets/1")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_ticket_requires_authorization(self):
        service = AsyncMock()
        service.delete_ticket.return_value = None

        app.dependency_overrides[ticket_routers.get_ticket_service] = lambda: service
        app.dependency_overrides[ticket_routers.get_uow] = lambda: DummyUoW()

        response = self.client.delete("/tickets/1")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
