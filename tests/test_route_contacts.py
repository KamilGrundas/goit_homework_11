import pytest
from unittest.mock import MagicMock, patch
from src.services.auth import auth_service


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