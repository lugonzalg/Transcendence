from . import models
from django.test import TestCase
from transcendence.settings import logger

def get_user_by_email(email: str) -> models.user_login | None:

    try:
        db_user = models.user_login.objects.filter(email=email).get()
        return db_user

    except Exception as err:
        logger.error(err)

# Create your tests here.
class CrudTest(TestCase):

    def test_get_user_by_email(self):

        self.assertEqual(get_user_by_email(None), None)
        self.assertEqual(get_user_by_email("test"), None)
