from urllib import response
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from requests import delete
from .forms import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .utils import *
import json
from fcm_django.models import FCMDevice
import pyotp
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from fcm_django.models import FCMDevice
from chat.models import ChatRoom
from core.messages import Message
# Create your views here.


class Registration(View):

    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        register = SignupForm(request.POST, request.FILES)
        if register.is_valid():
            email_from = settings.EMAIL_HOST_USER
            email = request.POST['email']
            otp = getotp()
            message = render_to_string("email.html", {'otp': otp['otp']})
            mail = EmailMultiAlternatives(
                subject='Verification',
                body=message,
                from_email=email_from,
                to=[email],
            )
            mail.attach_alternative(message, 'text/html')
            mail.send()
            return JsonResponse({"message": Message.OTP_SEND,
                                 "key": otp['key']})
        else:
            return JsonResponse({"erros": register.errors}, status=400)


class VerifyOtp(View):
    
    def post(self, request):
        register = SignupForm(data=request.POST, files=request.FILES)
        data = request.POST
        otp = data['otp']
        key = data['key']
        totp = pyotp.TOTP(key, interval=360)
        if totp.verify(otp):
            if register.is_valid():
                register.save()
                return JsonResponse({"messages":Message.REGISTRATION_DONE})
            else:
                return JsonResponse({"messages":Message.REGISTRATION_FAILED},
                                     status=404)
        else:
            return JsonResponse({"messages":Message.OTP_NOT_VALID}, 
                                 status=404)

class LoginUser(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.errors)
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(email=uname, password=upass)
            if user:
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'login.html', {'form': form})


class LogOut(View):
    
    def get(self, request):
        try:
            device = FCMDevice.objects.filter(user=request.user.id).last()
            device.delete()
        except:
            pass
        logout(request)
        return redirect("/")


class ForgetPassword(View):
    
    def post(self, request):
        user = User.objects.filter(email=request.POST['email'])
        if user:
            email=request.POST['email']
            email_from = settings.EMAIL_HOST_USER
            otp = getotp()
            message = render_to_string("email.html", {'otp': otp['otp']})
            mail = EmailMultiAlternatives(
                subject='Verification',
                body=message,
                from_email=email_from,
                to=[email],
            )
            mail.attach_alternative(message, 'text/html')
            mail.send()
            
            messages.add_message(request, 
                                 messages.SUCCESS, 
                                 Message.OTP_SEND)
            
            return render(request, "create_password.html", {"key":otp["key"],
                          "email":email})


class CreatePassword(View):
    
    def get(self, request):
        return render(request, "create_password.html")

    def post(self, request):
        data = request.POST
        totp = pyotp.TOTP(data['key'], interval=360)
        if totp.verify(data['otp']):
            upass = data['password']
            if upass.isalnum():
                upass = make_password(upass)
                user = User.objects.filter(email=data['email']).first()
                user.password = upass
                user.save()
                messages.add_message(request, messages.SUCCESS, 
                                     Message.CREATED_PASSWORD)
                return redirect('login')
            else:
                messages.add_message(request, 
                                    messages.ERROR, 
                                    Message.PASS_NUM_CHAR)
                return render(request, "create_password.html")
        else:
            messages.add_message(request, messages.ERROR, Message.OTP_INVALID)
            return render(request, "create_password.html")


class ChangePassword(View):
    
    def get(self, request):
        return render(request, "change_password.html")

    def post(self, request):
        data = request.POST
        old_pass = data['old-password']
        user = User.objects.filter(id=request.user.id).first()
        if user.check_password(old_pass):
            upass = data['password']
            if upass.isalnum():
                upass = make_password(upass)
                user.password = upass
                user.save()
                messages.add_message(request, messages.SUCCESS, 
                                    Message.CHANGE_PASS)
                return redirect('/')
            else:
                messages.add_message(request, 
                                        messages.ERROR, 
                                        Message.PASS_NUM_CHAR) 
                return render(request, "change_password.html")
        else:
            messages.add_message(request, messages.ERROR, 
                                Message.OLD_PASS_NOT_MATCH)


class UpdateProfile(View):
    
    def get(self, request):
        return render(request, "update_profile.html")

    def post(self, request):
        user = User.objects.filter(id=request.user.id).first()
        form = UpdateProfileForm(request.POST, 
                                request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 
                                "Profile Updated")
            return redirect('/')
        else:
            return render(request, 'update_profile.html', 
                            {"form":form})


class FollowingFollowers(View):
    
    def get(self, request, pk):
        if request.user.is_authenticated:
            user = User.objects.filter(id=pk).first()
            if user == request.user:
                messages.add_message(request, messages.ERROR, 
                                    Message.FOLLOW_YOUR_ID)
                return redirect(f"/user-info/{pk}")
            if user.follower.filter(id=request.user.id):
                user.follower.remove(request.user)
                request.user.following.remove(user)
                messages.add_message(request, messages.SUCCESS,
                                    Message.UNFOLLOW)
                return redirect(f"/user-info/{pk}")
            else:
                request.user.following.add(user)
                user.follower.add(request.user)
                if user.following.filter(id=request.user.id):
                    room = ChatRoom.objects.create()
                    room.room.add(user,request.user)
                messages.add_message(request, messages.SUCCESS,
                                     Message.FOLLOW)
                return redirect(f"/user-info/{pk}")


class UserInfo(View):
    
    def get(self, request, pk):
        user = User.objects.filter(id=pk).first()
        return render(request, 'userinfo.html', {"user": user})
        

class CreateUserDevice(View):
    
    def post(self, request):
        data = request.POST
        if FCMDevice.objects.filter(user=request.user).exists():
            return JsonResponse({"message": Message.IS_DEVICE})
        FCMDevice.objects.create(registration_id=data['registration_id'], 
                                    user=request.user, type=data['type'])
        return JsonResponse({"message": Message.CREATED_DEVICE})

