import pytest
from unittest.mock import MagicMock, patch
from src.services.auth import auth_service
from datetime import datetime, date, timedelta


def test_create_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contacts",
            json=  {
                    "forename": "Tomasz",
                    "surname": "Sędzikowski",
                    "email": "tomek@example.com",
                    "phone_number": "+48605123321",
                    "born_date": "2001-02-25",
                    },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["email"] == "tomek@example.com"
        assert "id" in data

def test_get_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "tomek@example.com"
        assert "id" in data

def test_get_contact_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_get_contacts(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["email"] == "tomek@example.com"
        assert "id" in data[0]


def test_update_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/1",
            json={
                    "forename": "Tomasz",
                    "surname": "Sędzikowski",
                    "email": "tomek_sedz@example.com",
                    "phone_number": "+48605123321",
                    "born_date": "2001-02-25",
                    },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "tomek_sedz@example.com"
        assert "id" in data

def test_update_contact_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/2",
            json={
                    "forename": "Wojciech",
                    "surname": "Sędzikowski",
                    "email": "wojtek@example.com",
                    "phone_number": "+4861051321",
                    "born_date": "2004-02-25",
                    },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_delete_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "tomek_sedz@example.com"
        assert "id" in data


def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_get_contact_got_birthday(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        today = date.today()
        client.post(
            "/api/contacts",
            json=  {
                    "forename": "Kamil",
                    "surname": "Cayld",
                    "email": "kamil.clayd@gmail.com",
                    "phone_number": "+48605412281",
                    "born_date": str(today + timedelta(days=2)),
                    },
            headers={"Authorization": f"Bearer {token}"}
        )
        client.post(
            "/api/contacts",
            json=  {
                    "forename": "Tadeusz",
                    "surname": "Romanowski",
                    "email": "tadek@example.com",
                    "phone_number": "+48601123421",
                    "born_date": str(today + timedelta(days=5)),
                    },
            headers={"Authorization": f"Bearer {token}"}
        )
        client.post(
            "/api/contacts",
            json=  {
                    "forename": "Patrycja",
                    "surname": "Bolgusz",
                    "email": "bolgusz_patrycja@example.com",
                    "phone_number": "+48664125551",
                    "born_date": str(today + timedelta(days=10)),
                    },
            headers={"Authorization": f"Bearer {token}"}
        )
        response = client.get(
            "/api/contacts/birthdays/",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 2

def test_get_contact_by_string(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/search/?search_by=Pat",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        assert data[0]["email"] == "bolgusz_patrycja@example.com"