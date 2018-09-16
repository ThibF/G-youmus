from unittest import TestCase
from unittest.mock import MagicMock

from users_push.usermanager import UserManager
from users_push.userstate import UserState


class TestUserManager(TestCase):
    def test_init_users(self):
        user_manager = UserManager()
        user_manager.users_librarian.init_users = MagicMock()
        user_manager.init_users()
        user_manager.users_librarian.init_users.assert_called_with()

    def test_is_new_user(self):
        user_manager = UserManager()
        user_state = UserState(42)
        user_manager.users_librarian.load_user = MagicMock(user_state)
        ret = user_manager.is_new_user(42)
        user_manager.users_librarian.load_user.assert_called_with(42)
        self.assertFalse(ret)

    def test_is_new_user_failed(self):
        user_manager = UserManager()
        user_state = UserState(42)
        user_manager.users_librarian.load_user = MagicMock(user_state)
        user_manager.users_librarian.load_user.side_effect = FileNotFoundError()
        ret = user_manager.is_new_user(42)
        user_manager.users_librarian.load_user.assert_called_with(42)
        self.assertTrue(ret)

    def test_create_user(self):
        user_manager = UserManager()
        user_manager.users_librarian.write_user = MagicMock()
        user_manager.user_hostess.greet_user = MagicMock()
        user_id = 42
        user_state = user_manager.create_user(user_id)

        user_manager.user_hostess.greet_user.assert_called_with(42)
        user_manager.users_librarian.write_user.assert_called_with(user_state)


"""
    def test_is_user_logged(self):
        self.fail()

    def test_verify_credentials(self):
        self.fail()

    def test_user_event(self):
        self.fail()

    def test_user_begin_identification(self):
        self.fail()

    def test_user_end_identification(self):
        self.fail()

    def test_ask_credentials(self):
        self.fail()
"""
