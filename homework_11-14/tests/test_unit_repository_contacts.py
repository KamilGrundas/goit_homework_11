import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from src.database.models import User, Contact
from src.schemas import ContactResponse
from src.database.models import User, Contact
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    get_contacts_got_birthday,
    get_contacts_with_string,
)
class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username='test_user')

    async def test_get_contacts(self):

        self.session.query().filter().all.return_value = [Contact(id=1, user_id=self.user.id), Contact(id=2, user_id=self.user.id)]
        result = await get_contacts(user=self.user, db=self.session)
        self.assertTrue(len(result) > 0) 


    async def test_get_contact_found(self):
        contact = Contact(id=1, user_id=self.user.id)
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=999, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        new_contact_data = ContactResponse(id=1, forename="John", surname="Doe", email="john.doe@example.com", phone_number="123456789", born_date=date.today())
        new_contact = Contact(**new_contact_data.dict(), user_id=self.user.id)
        self.session.add = MagicMock()
        self.session.commit = MagicMock()
        self.session.refresh = MagicMock(return_value=new_contact)
        result = await create_contact(body=new_contact_data, user=self.user, db=self.session)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertEqual(result.forename, new_contact_data.forename)
        self.assertEqual(result.surname, new_contact_data.surname)
        self.assertEqual(result.email, new_contact_data.email)

    async def test_remove_contact_found(self):
        contact = Contact(id=1, user_id=self.user.id)
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.session.delete.assert_called_once_with(contact)
        self.session.commit.assert_called_once()
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=999, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        original_contact = Contact(id=1, forename="John", surname="Doe", user_id=self.user.id)
        updated_data = ContactResponse(id=1, forename="Jane", surname="Doe", email="jane.doe@example.com", phone_number="987654321", born_date=date.today())
        self.session.query().filter().first.return_value = original_contact
        self.session.commit = MagicMock()
        result = await update_contact(contact_id=1, body=updated_data, user=self.user, db=self.session)
        self.session.commit.assert_called_once()
        self.assertEqual(result.forename, updated_data.forename)
        self.assertEqual(result.email, updated_data.email)

    async def test_update_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        updated_data = ContactResponse(
            id=999,
            forename="Jane", 
            surname="Doe", 
            email="jane.doe@example.com", 
            phone_number="987654321", 
            born_date=date.today()
        )

        result = await update_contact(contact_id=999, body=updated_data, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contacts_got_birthday(self):
        today = date.today()

        contact_with_upcoming_birthday = Contact(id=1, user_id=self.user.id, born_date=today + timedelta(days=3))
        contact_without_upcoming_birthday = Contact(id=2, user_id=self.user.id, born_date=today + timedelta(days=8))
        
        self.session.query().filter().all.return_value = [contact_with_upcoming_birthday]

        result = await get_contacts_got_birthday(user=self.user, db=self.session)

        self.assertIn(contact_with_upcoming_birthday, result)
        self.assertNotIn(contact_without_upcoming_birthday, result)


    async def test_get_contacts_with_string(self):

        matching_contact = Contact(id=1, user_id=self.user.id, forename="John", surname="Doe", email="johndoe@example.com")
        non_matching_contact = Contact(id=2, user_id=self.user.id, forename="Jane", surname="Smith", email="janesmith@example.com")
        
        search_string = "John"
        self.session.query().filter().all.return_value = [matching_contact]

        result = await get_contacts_with_string(search_by=search_string, user=self.user, db=self.session)

        self.assertIn(matching_contact, result)
        self.assertNotIn(non_matching_contact, result)



if __name__ == '__main__':
    unittest.main()
