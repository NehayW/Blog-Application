from email import message
from django.test import TestCase
from chat.models import ChatRoom, Message
from account.models import User
from datetime import datetime

class TestCases1(TestCase):
    def setUp(self):
        create_data = User.objects.create(first_name="djbfgddxln", 
                    last_name="any thing",
                    email="email@gmail.com",
                    date_joined=datetime.now())

        create_data1 = User.objects.create(first_name="djbfgddxln", 
                    last_name="any thing",
                    email="email2@gmail.com",
                    date_joined=datetime.now())
       
        chatroom = ChatRoom.objects.create()
        chatroom.room.add(create_data)
        chatroom.room.add(create_data1)

    def test_chat_model(self):
        chatroom = ChatRoom.objects.get(id=1)
        self.assertEqual(chatroom.room.count(),2)

class TestCases2(TestCase):
    def setUp(self):
        create_data = User.objects.create(first_name="djbfgddxln", 
                    last_name="any thing",
                    email="email3@gmail.com",
                    date_joined=datetime.now())

        create_data1 = User.objects.create(first_name="djbfgddxln", 
                    last_name="any thing",
                    email="email4@gmail.com",
                    date_joined=datetime.now())
       
        chatroom = ChatRoom.objects.create()
        chatroom.room.add(create_data)
        chatroom.room.add(create_data1)
        message = Message.objects.create(room_name=chatroom,
                                         auther=create_data,
                                         message="hello this is new message")
                                         

    def test_message_model(self):
        message = Message.objects.all().first()
        self.assertEqual(message.message, "hello this is new message")
    
    def test_auther_message(self):
        message = Message.objects.all().first()
        self.assertEqual(message.auther.email, "email3@gmail.com")
