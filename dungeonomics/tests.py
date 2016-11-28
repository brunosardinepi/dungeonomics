import unittest
from django.test import Client

class HomeTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get('home')
        self.assertEqual(response.status_code, 200)

# signup
# login
    # dungeonomics_test
    # 2YmP3sggAQ9p
# logout
# view campaign when not logged in
# view campaign while logged in
# crud campaign/monster/npc