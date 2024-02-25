import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)

class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.mock_user = User(id=1, email="test@example.com", username="testuser", confirmed=True, avatar="http://example.com/avatar.jpg")

    async def test_get_user_by_email_found(self):
        self.session.query().filter().first.return_value = self.mock_user
        result = await get_user_by_email("test@example.com", self.session)
        self.assertEqual(result, self.mock_user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email("notfound@example.com", self.session)
        self.assertIsNone(result)

    @patch('src.repository.users.Gravatar.get_image', return_value="http://example.com/new_avatar.jpg")
    async def test_create_user(self, mock_get_image):
        mock_user_data = UserModel(email="new@example.com", username="newuser", password="pass1234")
        new_user = await create_user(mock_user_data, self.session)
        self.session.add.assert_called_once()
        self.assertEqual(new_user.email, "new@example.com")
        self.assertTrue(mock_get_image.called)


    async def test_update_token(self):
        await update_token(self.mock_user, "new_refresh_token", self.session)
        self.assertEqual(self.mock_user.refresh_token, "new_refresh_token")
        self.session.commit.assert_called_once()

    async def test_confirmed_email(self):
        self.session.query().filter().first.return_value = self.mock_user
        await confirmed_email("test@example.com", self.session)
        self.assertTrue(self.mock_user.confirmed)
        self.session.commit.assert_called_once()

    async def test_update_avatar(self):
        new_avatar_url = "http://example.com/updated_avatar.jpg"
        self.session.query().filter().first.return_value = self.mock_user
        updated_user = await update_avatar("test@example.com", new_avatar_url, self.session)
        self.assertEqual(updated_user.avatar, new_avatar_url)
        self.session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
