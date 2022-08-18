from django.urls import path
from .views import *
from .feeds import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import blogSitemap

blogsitemap = {
"blog": blogSitemap, }

urlpatterns = [
    path('registration/', Registration.as_view(), name="registration"),
    path('verify-otp/', VerifyOtp.as_view(), name="verify-otp"),
    path('feed/', blogFeed(), name="feed"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', LogOut.as_view(), name="logout"),
    path('forgot-password/', ForgetPassword.as_view(), 
                             name="forgot-password"),
    path('change-password/', ChangePassword.as_view(), 
                             name="change-password"),
    path('create-forget-password/', CreatePassword.as_view(), 
                                    name='create-password'),
    path('update-profile/', UpdateProfile.as_view(), name='update-profile'),
    path('user-info/<int:pk>', UserInfo.as_view(), name="user-info"),
    path('follow-account/<int:pk>', FollowingFollowers.as_view(), 
                                    name="follower"),
    path('create-device', CreateUserDevice.as_view(), name="create-device"),
    path("sitemap.xml", sitemap, {"sitemaps": blogsitemap}, name="sitemap"),
    
    # path('post-details', PostView.as_view(), name="post-details")
]
