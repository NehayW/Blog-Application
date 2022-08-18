from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django.utils.translation import gettext as _


class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', )
    fieldsets = (
            (_("User Details"), {'fields': ('email', 'password')}),
            (_("Account Details"), {'fields': ('first_name', 'last_name', 
                                                'date_joined','profile_image',
                                                 'is_birthday',
                                                'is_active', 'is_staff', 
                                                'is_superuser', 'follower', 
                                                'following')}),
           )
    add_fieldsets = (
            ("User Details", {'classes': ('wide',), 
                              'fields':('email', 'password1', 
                                        'password2', 'first_name', 
                                        'last_name',  'is_staff', 
                                        'is_active', 'is_superuser',
                                        'is_birthday',
                                        'date_joined', 'profile_image',
                                        'follower', 'following',
                                        )}),
            
        )
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserVisit)