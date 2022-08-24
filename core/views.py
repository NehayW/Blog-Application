from inspect import ClassFoundException
from operator import imod
from django.shortcuts import render
from django.views import View
from post.models import *
from account.models import UserVisit
# Create your views here.


class HomePage(View):
    def get(self, request):
        if (request.user.is_authenticated and 
            not UserVisit.objects.filter(user=request.user.id).exists()):
            user = User.objects.filter(id=request.user.id).first()
            UserVisit.objects.create(url=request.path , user=user)
            return render(request, 'happy.html')
        posts = PostModel.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts":posts})


