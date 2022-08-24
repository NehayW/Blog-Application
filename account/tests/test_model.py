from venv import create
from django.test import TestCase
from account.models import User
from datetime import datetime

# Create your tests here.

class FirstTest(TestCase):

    def test_user(self):
        create_data = User.objects.create(first_name="djbfgddxln", 
                                   last_name="any thing",
                                   email="email@gmail.com",
                                   date_joined=datetime.now())
        self.assertTrue(isinstance(create_data, User))

    def test_user1(self):
        create_data = User.objects.create(password="")
        self.assertTrue(isinstance(create_data, User))
    
    def test_email(self):
        create_data = User.objects.create(email="")
        self.assertTrue(isinstance(create_data, User))
    
    def test_first_name(self):
        create_data = User.objects.create(first_name="165465")
        self.assertTrue(isinstance(create_data, User))

    def test_last_name(self):
        create_data = User.objects.create(last_name="484348")
        self.assertTrue(isinstance(create_data, User))

