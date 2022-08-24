from django.test import TestCase
from django.urls import reverse
from account.models import User

class Testview(TestCase):

    def setUp(self):
        user = User.objects.create(email='data@gmail.com',
                                   first_name='data1',
                                   password='data12345')

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse('room'), follow=True)
        self.assertEqual(response.status_code,200)


    def test_call_view_accept_user(self):
        self.client.login(username='data@gmail.com', password='data12345')
        response = self.client.get(reverse('room'))
        self.assertEqual(response.status_code, 302)