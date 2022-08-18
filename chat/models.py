from django.db import models
from account.models import User
# Create your models here.

class ChatRoom(models.Model):
    room = models.ManyToManyField(User, related_name="room")
    
class Message(models.Model):
    room_name = models.ForeignKey(ChatRoom, on_delete = models.CASCADE, 
                                  related_name="message")
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')        
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return self.message
    class Meta:
        ordering = ('timestamp',)
