from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('', HomePage.as_view(), name="homepage"), 
    path("firebase-messaging-sw.js",
        TemplateView.as_view(
            template_name="firebase-messaging-sw.js",
            content_type="application/javascript",
        ),
        name="firebase-messaging-sw.js"
    ),
]