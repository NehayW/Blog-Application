from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('registration/', Registration.as_view(), name="registration"),
    path('verify-otp/', VerifyOtp.as_view(), name="verify-otp"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', login_required(LogOut.as_view()), name="logout"),
    path('forgot-password/', ForgetPassword.as_view(), 
                             name="forgot-password"),
    path('change-password/', login_required(ChangePassword.as_view()), 
                             name="change-password"),
    path('create-forget-password/', CreatePassword.as_view(), 
                                    name='create-password'),
    path('update-profile/', login_required(UpdateProfile.as_view()), 
                            name='update-profile'),
    path('user-info/<int:pk>', login_required(UserInfo.as_view()), 
                                name="user-info"),
    path('follow-account/<int:pk>', 
          login_required(FollowingFollowers.as_view()), 
          name="follower"),
    path('create-device', login_required(CreateUserDevice.as_view()), 
                          name="create-device"),
]
