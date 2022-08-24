from django.test import TestCase
from django.urls import reverse
from account.models import User


class TestViews(TestCase):

    def setUp(self):
        pass

    def test_call_view_deny_anonymous(self):
        response = self.client.get(reverse('blogpost'), follow=True)
        self.assertEqual(response.status_code, 200)     

    
    def test_call_view_deny_anonymous1(self):
        response = self.client.get(reverse('mypost'), follow=True)
        self.assertEqual(response.status_code, 200) 
        response = self.client.post(reverse('mypost'), follow=True)
        self.assertEqual(response.status_code, 200) 


    def test_call_view_deny_anonymous2(self):
        response = self.client.get(reverse('postcomment'), follow=True)
        self.assertEqual(response.status_code, 200) 
        response = self.client.post(reverse('postcomment'), follow=True)
        self.assertEqual(response.status_code, 200) 

    def test_call_view_deny_anonymous3(self):
        response = self.client.get(reverse('replycomment'), follow=True)
        self.assertEqual(response.status_code, 200) 
        response = self.client.post(reverse('replycomment'), follow=True)
        self.assertEqual(response.status_code, 200)


class TestViewAfterLogin(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='data@gmail.com',
                                   first_name='data1',
                                   password='data12345')

    def test_call_view_accept_user(self):
        self.client.login(username='data@gmail.com', password='data12345')
        response = self.client.get(reverse('mypost'))
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'mypost.html')


    def test_call_view_accept_user1(self):
        self.client.login(username='data@gmail.com', password='data12345')
        response = self.client.get(reverse('postcomment'))
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'home.html')

    def test_call_view_accept_user2(self):
        self.client.login(username='data@gmail.com', password='data12345')
        response = self.client.get(reverse('replycomment'))
        self.assertEqual(response.status_code, 302)
