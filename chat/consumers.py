import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.auth import AuthMiddleware, AuthMiddlewareStack, UserLazyObject
from channels.auth import login, logout
from .models import *
from django.db.models import Q

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
        self.room_group_name,
        self.channel_name
        )

    def receive(self, text_data):
        self.user = self.scope["user"]
        login(self.scope, self.user, backend=None)
        self.scope["session"].save()
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender, receiver = text_data_json.get('sender'), text_data_json.get('receiver')
        sender = User.objects.filter(id=sender).first()
        receiver = User.objects.filter(id=receiver).first()
        room = ChatRoom.objects.filter(room=sender).filter(room=receiver).first()
        if not room:
            room = ChatRoom.objects.create()
            sender=User.objects.get(id=text_data_json['sender'])
            receiver=User.objects.get(id=text_data_json['receiver'])        
            room.room.add(sender,receiver)
        self.room_group_name = str(room.id)
       
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
        self.room_group_name,
        self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'chat_message',
            'message': message,
            'sender': sender,
            'receiver': receiver,
            'room': room,
            'receiver_image': sender
        }
        )
        sender=User.objects.get(id=text_data_json['sender'])
        if message.strip() != "":
            message=Message.objects.create(room_name=room, auther=sender, 
                                           message=message)
            message.save()

    # Receive message from room group
    def chat_message(self, event):
        self.user = self.scope["user"]
        username = event['sender'].id
        receiver = event['receiver'].id
        message = event['message']
        room = event['room'].id
        receiver_image =event['sender'].profile_image.url
        if message.strip() != "":
            self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'receiver': receiver,
            'room': room,
            'receiver_image':str(receiver_image)
            }))
