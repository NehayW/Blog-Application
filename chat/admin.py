from django.contrib import admin
from .models import *
# Register your models here.
from .models import *

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display: ('auther', 'message')


admin.site.register(ChatRoom)