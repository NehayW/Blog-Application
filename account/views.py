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
            # form.save()
            return JsonResponse({"message": "OTP has been sent"+
                                 "please check mail",
                                 "key": otp['key']})
        else:
            return JsonResponse({"erros": register.errors}, status=400)


class VerifyOtp(View):
    
    def post(self, request):
        # import pdb; pdb.set_trace()
        register = SignupForm(data=request.POST, files=request.FILES)
        # form = request.POST['data1']
        # print(form)
        # if form.is_valid():
        data = request.POST
        otp = data['otp']
        key = data['key']
        # register = SignupForm(request.POST['data1'])
        
            # data = (request.POST['data'])
            # form = (request.POST['form'])
            # print(form)
            # print("#######", data)
            # if form.is_valid():
            #     print("good to go")
            # print(request.POST['form'])
            # form = SignupForm(request.POST)
        totp = pyotp.TOTP(key, interval=360)
        if totp.verify(otp):
            if register.is_valid():
                register.save()
                
                # messages.add_message(request, messages.SUCCESS,
                #                     "registrations has been done")
                return JsonResponse({"messages":"registration has been done"})
            else:
                return JsonResponse({"messages":"registration has been failed "},
                                     status=404)
        else:
            # messages.add_message(request, messages.ERROR,
            #                         "OTP is Not valid try again ")
            return JsonResponse({"messages":"OTP is Not valid try again"}, 
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
        if request.user.is_authenticated:
            try:
                device = FCMDevice.objects.filter(user=request.user.id).last()
                device.delete()
            except:
                pass
            logout(request)
            return redirect("/")
        else:
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
                                 "OTP has been sent to your mail")
            
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
                                    "Password has been created")
                return redirect('login')
            else:
                messages.add_message(request, 
                                    messages.ERROR, 
                                    "Password shoud contain a num and a char")
                return render(request, "create_password.html")
        else:
            messages.add_message(request, messages.ERROR, "Invalid OTP")
            return render(request, "create_password.html")


class ChangePassword(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "change_password.html")
        else:
            return redirect('login')
    
    def post(self, request):
        if request.user.is_authenticated:
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
                                        "Password has been Changed")
                    return redirect('/')
                else:
                    messages.add_message(request, 
                                         messages.ERROR, 
                                         "Password shoud contain a"+ 
                                         "num and a char") 
                    return render(request, "change_password.html")
            else:
                messages.add_message(request, messages.ERROR, 
                                    "Old password did't match")
        else:
            return redirect("login")


class UpdateProfile(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "update_profile.html")
        else:
            return redirect("login")
    
    def post(self, request):
        if request.user.is_authenticated:
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
        else:
            return redirect('login')


class FollowingFollowers(View):
    
    def get(self, request, pk):
        if request.user.is_authenticated:
            user = User.objects.filter(id=pk).first()
            if user == request.user:
                messages.add_message(request, messages.ERROR, 
                                    "You can not follow your id")
                return redirect(f"/user-info/{pk}")
            if user.follower.filter(id=request.user.id):
                user.follower.remove(request.user)
                request.user.following.remove(user)
                messages.add_message(request, messages.SUCCESS,
                                    "You unfollow this user")
                return redirect(f"/user-info/{pk}")
            else:
                request.user.following.add(user)
                user.follower.add(request.user)
                if user.following.filter(id=request.user.id):
                    room = ChatRoom.objects.create()
                    room.room.add(user,request.user)
                messages.add_message(request, messages.SUCCESS,
                                     "You follow this user")
                return redirect(f"/user-info/{pk}")


class UserInfo(View):
    
    def get(self, request, pk):
        user = User.objects.filter(id=pk).first()
        return render(request, 'userinfo.html', {"user": user})
        
class MyFollowers(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.filter(id=request.user.id).first()
            return render(request, "followers.html", {"user": user})

class MyFollowing(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.filter(id=request.user.id).first()
            return render(request, "following.html", {"user": user})


class CreateUserDevice(View):
    
    def post(self, request):
        if request.user.is_authenticated:
            data = request.POST
            if FCMDevice.objects.filter(user=request.user).exists():
                return JsonResponse({"message": "Device Already Created"})
            FCMDevice.objects.create(registration_id=data['registration_id'], 
                                     user=request.user, type=data['type'])
            return JsonResponse({"message": "Device Created"})
        return JsonResponse({"message": "Device Not created"})
