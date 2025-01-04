from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import server, get_db
from app.models import Item


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_db_override():
        return session

    server.dependency_overrides[get_db] = get_db_override
    client = TestClient(server)
    mock_response = {'reservation_id': 222}
    with patch("app.main.call_reservation_api", new=AsyncMock(return_value=mock_response)):
        yield client
    server.dependency_overrides.clear()


def test_post_item(client: TestClient):
    """ Test posting an item """
    response = client.post(
        "/items/", json={"name": "hat", "quantity": 2}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "hat"
    assert data["quantity"] == 2


def test_id_overwrite_protection(client: TestClient):
    """ Tests if the id is ignored by the database engine if provided by the post request."""
    client.post(
        "/items/", json={"id": 1, "name": "hat", "quantity": 2}
    )
    response = client.post(
        "/items/", json={"id": 1, "name": "pants", "quantity": 4}
    )
    data = response.json()
    assert data['id'] == 2


def test_invalid_quantity(client: TestClient):
    """ Tests if the proper 422 error is sent when adding an item with quantity 0. """
    response = client.post(
        "/items/", json={"name": "hat", "quantity": 0}
    )
    assert response.status_code == 422


def test_read_get_items(session: Session, client: TestClient):
    """ Tests the functionality of the get_item_list function. """
    hat = Item(name="hat", quantity=2)
    pant = Item(name="pant", quantity=4)
    session.add(hat)
    session.add(pant)
    session.commit()

    response = client.get("/items/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == hat.name
    assert data[0]["quantity"] == hat.quantity
    assert data[1]["name"] == pant.name
    assert data[1]["quantity"] == pant.quantity
