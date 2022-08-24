
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin 
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import UserAccountManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name =models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(upload_to='media/image/profile',
                                        null=True, blank=True,
                                        )
    follower = models.ManyToManyField("self", related_name="followers",
                                         blank=True, symmetrical=False, 
                                       )
    following = models.ManyToManyField("self", related_name="followings", 
                                        blank=True, symmetrical=False,
                                        )
    # is_birthday = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", kwargs = {"id": self.id})


class UserVisit(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name
